export function formatDatetime(datetime) {
  const date = new Date(datetime);
  const now = new Date();

  // 한국 시간으로 변환
  const koreaDate = new Date(date.getTime() + 9 * 60 * 60 * 1000);
  const koreaNow = new Date(now.getTime() + 9 * 60 * 60 * 1000);

  // 날짜 차이 계산
  const diffDays = koreaNow.getDate() - koreaDate.getDate();


  // 하루가 지나지 않았으면 시간만 표시
  if (diffDays === 0) {
    const options = { hour: 'numeric', minute: 'numeric', hour12: true };
    return koreaDate.toLocaleString('ko-KR', options);
  }

  // 하루가 지났으면 '어제' 표시
  if (diffDays === 1) {
    return "어제";
  }

  // 이틀 이상 지났으면 YYYY-MM-DD 형식으로 표시
  return koreaDate.toISOString().split("T")[0];
}