const user_id = Math.floor(Math.random() * 1000000).toString();
document.getElementById("user_id").innerText = "ID: " + user_id;

async function loadUser() {
    const res = await fetch(`/get_user/${user_id}`);
    const data = await res.json();
    document.getElementById("balance").innerText = data.balance;
}

async function addCoins() {
    const res = await fetch("/update_balance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, amount: 100 })
    });
    const data = await res.json();
    document.getElementById("balance").innerText = data.balance;
}

function mine() {
    alert("⛏ Mayning boshlanmoqda...");
    addCoins();
}

loadUser();
console.log("Tanga mini ilova yuklandi ✅");
