export async function fetchQueue(roomId, trackId = '') {
  const response = await fetch(`/api/rooms/${roomId}/queue?track_id=${trackId}`);
  return await response.json();
}

export function formatParticipants(participants) {
  return Object.entries(participants).map(([id, name]) => ({ id, name }));
}
