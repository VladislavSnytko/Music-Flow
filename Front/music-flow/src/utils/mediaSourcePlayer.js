export async function loadWithMediaSource(audioElement, url) {
  if (!window.MediaSource || !MediaSource.isTypeSupported('audio/mpeg')) {
    audioElement.src = url;
    await audioElement.load();
    return;
  }

  return new Promise((resolve, reject) => {
    const mediaSource = new MediaSource();
    audioElement.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', async () => {
      try {
        const sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
        sourceBuffer.mode = 'sequence';

        let queue = [];
        let updating = false;
        const append = (chunk) => {
          if (!updating) {
            updating = true;
            sourceBuffer.appendBuffer(chunk);
          } else {
            queue.push(chunk);
          }
        };

        sourceBuffer.addEventListener('updateend', () => {
          updating = false;
          if (queue.length > 0) {
            append(queue.shift());
          } else if (mediaSource.readyState === 'open' && !audioElement.error) {
            mediaSource.endOfStream();
            resolve();
          }
        });

        const response = await fetch(url);
        const reader = response.body.getReader();

        const read = async () => {
          const { done, value } = await reader.read();
          if (done) {
            if (!updating) {
              mediaSource.endOfStream();
              resolve();
            }
            return;
          }
          append(value);
          read();
        };

        read();
      } catch (e) {
        reject(e);
      }
    });

    audioElement.load();
  });
}
