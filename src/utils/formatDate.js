export function formatDatetime(datetime) {
  const date = new Date(datetime); // 주어진 날짜 (UTC)
  const now = new Date();

  // 날짜 비교를 위해 한국 시간으로 변환
  const koreaDate = new Date(date.getTime() +  60 * 60 * 1000);
  const koreaNow = new Date(now.getTime() + 60 * 60 * 1000);

  // 날짜가 다르면 "어제"로 표시
  if (
    koreaNow.getFullYear() === koreaDate.getFullYear() &&
    koreaNow.getMonth() === koreaDate.getMonth() &&
    koreaNow.getDate() - koreaDate.getDate() === 1
  ) {
    return "어제";
  }

  // 같은 날이면 오전/오후 시:분 표시
  if (
    koreaNow.getFullYear() === koreaDate.getFullYear() &&
    koreaNow.getMonth() === koreaDate.getMonth() &&
    koreaNow.getDate() === koreaDate.getDate()
  ) {
    const options = { hour: "numeric", minute: "numeric", hour12: true };
    return date.toLocaleString("ko-KR", options);
  }

  // 이틀 이상 지났으면 YYYY-MM-DD 형식으로 표시
  const year = koreaDate.getFullYear();
  const month = (koreaDate.getMonth() + 1).toString().padStart(2, "0");
  const day = koreaDate.getDate().toString().padStart(2, "0");
  return `${year}-${month}-${day}`;
}
