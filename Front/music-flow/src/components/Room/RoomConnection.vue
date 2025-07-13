<script>
import { ref, onMounted, onUnmounted } from 'vue'
import useRoomService from './room-service'

export default {
  props: {
    roomId: {
      type: String,
      required: true
    },
    userId: {
      type: String,
      required: true
    }
  },

  setup(props, { emit }) {
    const { connect, disconnect, sendCommand } = useRoomService()

    const participants = ref([])
    const currentTrack = ref(null)
    const trackQueue = ref([])

    onMounted(() => {
      connect(props.roomId, props.userId, {
        onTrackUpdate: (track) => {
          currentTrack.value = track
          emit('track-update', track)
        },
        onQueueUpdate: (queue) => {
          trackQueue.value = queue
          emit('queue-update', queue)
        },
        onParticipantsUpdate: (users) => {
          participants.value = users
          emit('participants-update', users)
        }
      })
    })

    onUnmounted(() => {
      disconnect()
    })

    return {
      participants,
      currentTrack,
      trackQueue,
      sendCommand
    }
  }
}
</script>