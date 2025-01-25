export function formatDatetime(datetime) {
  const date = new Date(datetime);
  const options = { hour: 'numeric', minute: 'numeric', hour12: true };
  return date.toLocaleString('ko-KR', options);
}