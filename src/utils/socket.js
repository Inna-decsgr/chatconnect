import { io } from "socket.io-client";

const socket = io("http://localhost:5000"); // Flask 서버 주소

socket.on("connect", () => {
  console.log("✅ Connected to server!");
});

socket.on("disconnect", () => {
  console.log("❌ Disconnected from server.");
});

socket.on("response", (data) => {
  console.log("📩 Server response:", data);
});

export default socket;
