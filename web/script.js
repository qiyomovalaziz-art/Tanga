let tg = window.Telegram.WebApp;
tg.expand();

const user = tg.initDataUnsafe?.user;
const user_id = user?.id || Math.floor(Math.random() * 1000000);
document.getElementById("name").innerText = user?.first_name || "Foydalanuvchi";

async function getUser() {
  let res = await fetch(`/api/user/${user_id}`);
  let data = await res.json();
  document.getElementById("balance").innerText = data.balance.toFixed(3) + " ₽";
}
getUser();

document.getElementById("collect").addEventListener("click", async () => {
  let res = await fetch("/api/collect", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({user_id})
  });
  let data = await res.json();
  tg.showAlert(`💰 Balansga ${data.added.toFixed(3)} ₽ qo‘shildi!`);
  document.getElementById("balance").innerText = data.new_balance.toFixed(3) + " ₽";
});

document.getElementById("bonus").addEventListener("click", async () => {
  let res = await fetch("/api/bonus", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({user_id})
  });
  let data = await res.json();
  tg.showAlert(data.message);
  getUser();
});
