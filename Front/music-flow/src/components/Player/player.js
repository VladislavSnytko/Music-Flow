import { ref, watch } from 'vue'

export default function usePlayer(initialTrack) {
  const audioElement = ref(null)
  const currentTrack = ref(initialTrack)
  const isPlaying = ref(false)
  const progress = ref(0)
  const duration = ref(0)

  // Инициализация аудио элемента
  const initAudio = () => {
    if (!audioElement.value) return

    audioElement.value.addEventListener('timeupdate', () => {
      progress.value = audioElement.value.currentTime
    })

    audioElement.value.addEventListener('durationchange', () => {
      duration.value = audioElement.value.duration
    })

    audioElement.value.addEventListener('ended', nextTrack)
  }

  // Загрузка трека
  const loadTrack = (track) => {
    if (!audioElement.value) return
    
    currentTrack.value = track
    audioElement.value.src = track.audioSrc
    if (isPlaying.value) {
      audioElement.value.play()
    }
  }

  // Управление воспроизведением
  const togglePlay = () => {
    if (!audioElement.value) return
    
    if (isPlaying.value) {
      audioElement.value.pause()
    } else {
      audioElement.value.play()
    }
    isPlaying.value = !isPlaying.value
  }

  const seek = (time) => {
    if (!audioElement.value) return
    audioElement.value.currentTime = time
  }

  const prevTrack = () => {
    // Логика переключения на предыдущий трек
    // Можно эмитить событие или вызывать метод извне
  }

  const nextTrack = () => {
    // Логика переключения на следующий трек
  }

  // Инициализация при монтировании
  watch(audioElement, initAudio, { immediate: true })

  return {
    audioElement,
    currentTrack,
    isPlaying,
    progress,
    duration,
    togglePlay,
    prevTrack,
    nextTrack,
    seek,
    loadTrack
  }
}