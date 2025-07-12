import { useState } from 'react'

function App() {
  const [input, setInput] = useState("")
  const [messages, setMessages] = useState([])

  async function sendMessage() {
    if (!input.trim()) return

    const userMessage = { sender: "user", text: input }
    setMessages([...messages, userMessage])

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    })
    const data = await res.json()
    setMessages(prev => [...prev, { sender: "bot", text: data.reply }])
    setInput("")
  }

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h1>SolaceBot</h1>
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: 8,
          padding: 10,
          height: "60vh",
          overflowY: "auto",
          marginBottom: 10,
        }}
      >
        {messages.map((m, i) => (
          <div key={i} style={{ margin: "10px 0", textAlign: m.sender === "user" ? "right" : "left" }}>
            <b>{m.sender === "user" ? "You" : "SolaceBot"}</b>: {m.text}
          </div>
        ))}
      </div>
      <input
        style={{ width: "80%", padding: 8 }}
        type="text"
        value={input}
        placeholder="Say something..."
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={e => { if (e.key === "Enter") sendMessage() }}
      />
      <button onClick={sendMessage} style={{ padding: 8, marginLeft: 10 }}>
        Send
      </button>
    </div>
  )
}

export default App

