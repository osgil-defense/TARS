import React, { useState, useEffect, useRef } from "react";
import {
  BrowserRouter as Router,
  Route,
  Link,
  Routes,
  Navigate,
} from "react-router-dom";
import {
  Terminal,
  Send,
  User,
  Info,
  MessageSquare,
  Code,
  Bot,
} from "lucide-react";
import OpenAI from "openai";

// import LoginPage from "./components/LoginPage";
import ChatInterface from "./components/ChatInterface";

// Global variable to store message history
let globalMessageHistory = [];

export const Header = () => {
  const aboutUrl = "https://www.osgil.org/";

  return (
    <header className="bg-gray-800 h-12 px-2 flex justify-between items-center fixed top-0 left-0 right-0 z-10">
      <div className="flex items-center h-full">
        <img src="/logo.png" alt="Logo" className="h-6 w-6 mr-2" />
        <Link to="/" className="text-white text-lg font-bold">
          TARS
        </Link>
      </div>
      <nav className="h-full">
        <ul className="flex h-full items-center">
          <li className="h-full">
            <a
              href={aboutUrl}
              className="text-white hover:text-gray-300 text-sm flex items-center h-full px-3"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Info size={14} className="mr-1" />
              About
            </a>
          </li>
        </ul>
      </nav>
    </header>
  );
};

const App = () => {
  const [messages, setMessages] = useState(globalMessageHistory);
  const [terminalOutput, setTerminalOutput] = useState(
    "Welcome to the terminal view!\n",
  );
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState("");

  const openai = new OpenAI({
    apiKey: process.env.REACT_APP_OPENAI_API_KEY,
    dangerouslyAllowBrowser: true,
  });

  const handleSendMessage = async (message) => {
    const updatedMessages = [...messages, { text: message, isUser: true }];
    setMessages(updatedMessages);
    globalMessageHistory = updatedMessages;
    setIsLoading(true);
    setTerminalOutput((prev) => `${prev}\n$ Processing message...\n`);
    setStreamingMessage("");

    try {
      const apiMessages = globalMessageHistory.map((msg) => ({
        role: msg.isUser ? "user" : "assistant",
        content: msg.text,
      }));

      const stream = await openai.chat.completions.create({
        model: "gpt-4",
        messages: apiMessages,
        stream: true,
      });

      let fullResponse = "";
      for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content || "";
        fullResponse += content;
        setStreamingMessage((prev) => prev + content);
      }

      const newUpdatedMessages = [
        ...updatedMessages,
        { text: fullResponse, isUser: false },
      ];
      setMessages(newUpdatedMessages);
      globalMessageHistory = newUpdatedMessages;
      setStreamingMessage("");
      setTerminalOutput((prev) => `${prev}Response generated.\n`);
    } catch (error) {
      console.error("Error generating response:", error);
      setTerminalOutput((prev) => `${prev}Error generating response.\n`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Router>
      <div className="flex flex-col h-screen bg-gray-900 text-white">
        <Header />
        <main className="flex-grow overflow-hidden pt-12">
          <Routes>
            <Route
              path="/"
              element={
                <ChatInterface
                  handleSendMessage={handleSendMessage}
                  messages={messages}
                  isLoading={isLoading}
                  terminalOutput={terminalOutput}
                  streamingMessage={streamingMessage}
                />
              }
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
