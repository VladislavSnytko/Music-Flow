const controllers = new WeakMap();

export async function loadWithMediaSource(audioElement, streamUrl) {
  // Отменяем предыдущую загрузку
  const prev = controllers.get(audioElement);
  if (prev) {
    prev.abort();
    controllers.delete(audioElement);
  }

  const isMp3 = /\.mp3(\?.*)?$/i.test(streamUrl);
  if (!window.MediaSource || isMp3 || !MediaSource.isTypeSupported('audio/mpeg')) {
    audioElement.src = streamUrl;
    return;
  }

  const controller = new AbortController();
  controllers.set(audioElement, controller);
  const mediaSource = new MediaSource();
  const objectUrl = URL.createObjectURL(mediaSource);
  
  // Сбрасываем предыдущие обработчики
  audioElement.src = '';
  audioElement.load();
  audioElement.src = objectUrl;
  audioElement.load();

  const onEnded = () => {
    URL.revokeObjectURL(objectUrl);
    audioElement.removeEventListener('ended', onEnded);
  };
  audioElement.addEventListener('ended', onEnded);

  mediaSource.addEventListener('sourceopen', () => {
    const sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
    sourceBuffer.mode = 'sequence';

    let queue = [];
    let updating = false;
    let readerDone = false;
    let initialDurationSet = false;

    const safeSetDuration = (duration) => {
      if (!updating && mediaSource.readyState === 'open') {
        try {
          mediaSource.duration = duration;
          audioElement.duration = duration;
        } catch (e) {
          console.warn('Could not set duration:', e);
        }
      }
    };

    sourceBuffer.addEventListener('updatestart', () => {
      updating = true;
    });

    sourceBuffer.addEventListener('updateend', () => {
      updating = false;
      
      if (!initialDurationSet && mediaSource.duration === Infinity) {
        safeSetDuration(0);
        initialDurationSet = true;
      }

      if (queue.length > 0) {
        updating = true;
        sourceBuffer.appendBuffer(queue.shift());
      } else if (readerDone) {
        mediaSource.endOfStream();
        // После окончания загрузки устанавливаем финальную длительность
        safeSetDuration(audioElement.duration);
      }
    });

    sourceBuffer.addEventListener('error', () => {
      console.error('SourceBuffer error:', sourceBuffer.error);
    });

    fetch(streamUrl, { signal: controller.signal })
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const reader = response.body.getReader();
        let totalBytes = 0;
        
        function pump() {
          return reader.read().then(({ done, value }) => {
            if (done) {
              readerDone = true;
              if (!updating && mediaSource.readyState === 'open') {
                mediaSource.endOfStream();
              }
              return;
            }
            
            totalBytes += value.byteLength;
            queue.push(value);
            
            // Периодически обновляем длительность на основе загруженных данных
            if (totalBytes % (1024 * 512) === 0) { // Каждые 512KB
              safeSetDuration(totalBytes / (1024 * 128)); // Примерная оценка
            }

            if (!updating) {
              updating = true;
              sourceBuffer.appendBuffer(queue.shift());
            }
            return pump();
          });
        }
        return pump();
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          console.error('MSE fetch error:', err);
          mediaSource.endOfStream();
        }
      });
  });

  // Обработчик ошибок MediaSource
  mediaSource.addEventListener('sourceended', () => {
    if (mediaSource.readyState === 'ended') {
      audioElement.dispatchEvent(new Event('durationchange'));
    }
  });

  mediaSource.addEventListener('sourceclose', () => {
    URL.revokeObjectURL(objectUrl);
  });
}