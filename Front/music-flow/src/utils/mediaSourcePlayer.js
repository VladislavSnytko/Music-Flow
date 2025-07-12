export async function loadWithMediaSource(audioElement, url) {
  if (!window.MediaSource) {
    audioElement.src = url;
    await audioElement.load();
    return;
  }

  const mediaSource = new MediaSource();
  audioElement.src = URL.createObjectURL(mediaSource);

  mediaSource.addEventListener('sourceopen', async () => {
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    const mime = response.headers.get('content-type') || 'audio/mpeg';
    const sourceBuffer = mediaSource.addSourceBuffer(mime);
    sourceBuffer.addEventListener('updateend', () => {
      mediaSource.endOfStream();
    });
    sourceBuffer.appendBuffer(arrayBuffer);
  });
}
