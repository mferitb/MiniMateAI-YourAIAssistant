document.getElementById("send_button").addEventListener("click", sendMessage)
document.getElementById("user_input").addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    sendMessage()
  }
})

async function sendMessage() {
  const userInput = document.getElementById("user_input").value
  if (userInput.trim() === "") return

  const chatlog = document.getElementById("chatlog")
  chatlog.innerHTML += `<div class="user-message">${userInput}</div>`
  document.getElementById("user_input").value = ""
  chatlog.scrollTop = chatlog.scrollHeight

  // Add typing indicator
  const typingIndicator = document.createElement("div")
  typingIndicator.className = "typing-indicator"
  typingIndicator.innerHTML = `<span></span><span></span><span></span>`
  chatlog.appendChild(typingIndicator)
  chatlog.scrollTop = chatlog.scrollHeight

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userInput }),
    })

    const data = await response.json()

    // Remove typing indicator
    chatlog.removeChild(typingIndicator)

    chatlog.innerHTML += `<div class="bot-message">${data.reply}</div>`
    chatlog.scrollTop = chatlog.scrollHeight
  } catch (error) {
    // Remove typing indicator
    chatlog.removeChild(typingIndicator)

    chatlog.innerHTML += `<div class="bot-message">Hata oluştu: ${error.message}</div>`
    chatlog.scrollTop = chatlog.scrollHeight
  }
}

// Focus input field when page loads
window.onload = () => {
  document.getElementById("user_input").focus()
}
