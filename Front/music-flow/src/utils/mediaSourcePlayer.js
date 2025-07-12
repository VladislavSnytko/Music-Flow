let currentAbortController = null;

export async function loadWithMediaSource(audioElement, url) {
  if (!window.MediaSource || !MediaSource.isTypeSupported('audio/mpeg')) {
    audioElement.src = url;
    await audioElement.load();
    return;
  }

  if (currentAbortController) {
    currentAbortController.abort();
  }

  const abortController = new AbortController();
  currentAbortController = abortController;

  return new Promise((resolve, reject) => {
    const mediaSource = new MediaSource();
    audioElement.src = URL.createObjectURL(mediaSource);

    const cleanup = () => {
      if (currentAbortController === abortController) {
        currentAbortController = null;
      }
    };

    mediaSource.addEventListener('sourceopen', async () => {
      try {
        const sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
        sourceBuffer.mode = 'sequence';

        let queue = [];
        let updating = false;
        const append = (chunk) => {
          if (abortController.signal.aborted) return;
          if (!updating) {
            updating = true;
            sourceBuffer.appendBuffer(chunk);
          } else {
            queue.push(chunk);
          }
        };

        sourceBuffer.addEventListener('updateend', () => {
          if (abortController.signal.aborted) return;
          updating = false;
          if (queue.length > 0) {
            append(queue.shift());
          } else if (mediaSource.readyState === 'open' && !audioElement.error) {
            mediaSource.endOfStream();
            cleanup();
            resolve();
          }
        });

        const response = await fetch(url, { signal: abortController.signal });
        const reader = response.body.getReader();

        const read = async () => {
          const { done, value } = await reader.read();
          if (abortController.signal.aborted) return;
          if (done) {
            if (!updating) {
              mediaSource.endOfStream();
              cleanup();
              resolve();
            }
            return;
          }
          append(value);
          read();
        };

        read();
      } catch (e) {
        cleanup();
        if (!abortController.signal.aborted) {
          reject(e);
        }
      }
    });

    audioElement.load();
  });
}
