let currentSession = null;

export async function loadWithMediaSource(audioElement, url) {
  if (!window.MediaSource || !MediaSource.isTypeSupported('audio/mpeg')) {
    // Fallback for browsers without MediaSource support
    audioElement.src = url;
    await audioElement.load();
    return;
  }

  // Cancel any previous load session
  if (currentSession) {
    currentSession.abort();
    currentSession = null;
  }

  const session = {
    aborted: false,
    abortController: new AbortController(),
    mediaSource: new MediaSource(),
    objectUrl: null,
    sourceBuffer: null,

    abort() {
      this.aborted = true;
      this.abortController.abort();
      try {
        if (this.sourceBuffer && this.mediaSource.readyState === 'open') {
          this.mediaSource.removeSourceBuffer(this.sourceBuffer);
        }
        if (this.mediaSource.readyState === 'open') {
          this.mediaSource.endOfStream();
        }
      } catch (e) {
        console.warn('Cleanup error:', e);
      }
      if (this.objectUrl) {
        URL.revokeObjectURL(this.objectUrl);
      }
    }
  };

  currentSession = session;
  session.objectUrl = URL.createObjectURL(session.mediaSource);
  audioElement.src = session.objectUrl;

  return new Promise((resolve, reject) => {
    const onError = (error) => {
      if (session.aborted) return;
      session.abort();
      reject(error);
    };

    session.mediaSource.addEventListener('sourceopen', async () => {
      if (session.aborted) return;

      try {
        session.sourceBuffer = session.mediaSource.addSourceBuffer('audio/mpeg');
        session.sourceBuffer.mode = 'sequence';

        let queue = [];
        let updating = false;

        const appendChunk = (chunk) => {
          if (session.aborted) return;

          if (!updating && session.mediaSource.readyState === 'open') {
            try {
              updating = true;
              session.sourceBuffer.appendBuffer(chunk);
            } catch (e) {
              onError(e);
            }
          } else {
            queue.push(chunk);
          }
        };

        session.sourceBuffer.addEventListener('updateend', () => {
          if (session.aborted) return;

          updating = false;
          if (queue.length > 0) {
            appendChunk(queue.shift());
          } else if (session.mediaSource.readyState === 'open') {
            try {
              session.mediaSource.endOfStream();
              resolve();
            } catch (e) {
              onError(e);
            }
          }
        });

        session.sourceBuffer.addEventListener('error', () => {
          onError(new Error('SourceBuffer error'));
        });

        const response = await fetch(url, {
          signal: session.abortController.signal
        });
        const reader = response.body.getReader();

        const readChunks = async () => {
          try {
            const { done, value } = await reader.read();
            if (session.aborted) return;

            if (done) {
              if (!updating && session.mediaSource.readyState === 'open') {
                session.mediaSource.endOfStream();
                resolve();
              }
              return;
            }

            appendChunk(value);
            readChunks();
          } catch (e) {
            if (!session.aborted) {
              onError(e);
            }
          }
        };

        readChunks();
      } catch (e) {
        onError(e);
      }
    });

    session.mediaSource.addEventListener('sourceclose', () => {
      if (!session.aborted) {
        onError(new Error('MediaSource closed unexpectedly'));
      }
    });

    audioElement.addEventListener('error', () => {
      onError(new Error('Audio element error'));
    });

    audioElement.load();
  });
}
