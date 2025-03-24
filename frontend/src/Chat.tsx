import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
  const [messages, setMessages] = useState<{ role: string, text: string }[]>([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    const res = await axios.post('http://localhost:8000/chat', {
      message: input
    });

    const botReply = res.data.reply;
    setMessages(prev => [...prev, { role: 'assistant', text: botReply }]);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-4">
      <h1 className="text-2xl font-bold mb-4">Dream Agent Chat</h1>
      <div className="w-full max-w-xl bg-gray-800 p-4 rounded-xl space-y-2 overflow-y-auto h-96">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role === 'user' ? 'text-right' : 'text-left'}>
            <span className="block bg-gray-700 rounded-lg px-3 py-2 inline-block">
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <div className="flex w-full max-w-xl mt-4">
        <input
          className="flex-1 p-2 rounded-l-lg bg-gray-700 text-white"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Напиши сообщение..."
        />
        <button onClick={sendMessage} className="bg-blue-600 px-4 rounded-r-lg">Отправить</button>
      </div>
    </div>
  );
};

export default Chat;