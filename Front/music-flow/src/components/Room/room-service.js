import { ref } from 'vue'

export default function useRoomService() {
  const socket = ref(null)

  const connect = (roomId, userId, callbacks) => {
    socket.value = new WebSocket(`/ws/room/${roomId}/ws?user_id=${userId}`)

    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      switch(data.type) {
        case 'track_state':
          callbacks.onTrackUpdate(data.track)
          break
        case 'queue_update':
          callbacks.onQueueUpdate(data.queue)
          break
        case 'participants_update':
          callbacks.onParticipantsUpdate(data.participants)
          break
      }
    }
  }

  const disconnect = () => {
    if (socket.value) {
      socket.value.close()
      socket.value = null
    }
  }

  const sendCommand = (command) => {
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify(command))
    }
  }

  return {
    connect,
    disconnect,
    sendCommand
  }
}