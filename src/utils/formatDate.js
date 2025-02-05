export function formatDatetime(datetime) {
  const date = new Date(datetime);  // 주어진 날짜 UTC
  const now = new Date();


  // 일리초 단위 차이 계산(24시간 단위 변환)
  const diffTime = now.getTime() - date.getTime(); // 밀리초 차이
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24)); // 하루 단위로 계산


  // 하루가 지나지 않았다면 오전/오후 시:분
  if (diffDays === 0) {
    const options = { hour: 'numeric', minute: 'numeric', hour12: true };
    return date.toLocaleString('ko-KR', options);
  }

  // 하루가 지났다면 '어제'
  if (diffDays === 1) {
    return "어제";
  }

  // 이틀 이상 지났으면 YYYY-MM-DD 형식으로 표시
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, "0"); // 두 자리로 변환
  const day = date.getDate().toString().padStart(2, "0"); // 두 자리로 변환
  return `${year}-${month}-${day}`;

}

