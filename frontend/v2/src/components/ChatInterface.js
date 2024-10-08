import React, { useEffect, useRef, useState } from "react";
import {
  Send,
  Terminal,
  MessageSquare,
  Code,
  Zap,
  Layout,
  Globe,
  Server,
  Database,
  Lock,
  Smartphone,
  Cloud,
  GitBranch,
  Cpu,
  Box,
  Webhook,
  Fingerprint,
  Network,
  Binary,
  Layers,
  Gauge,
  Bug,
  GitCommit,
  FileJson,
  Puzzle,
  Lightbulb,
  RefreshCw,
  ChevronDown,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import remarkGfm from "remark-gfm";

export const ChatInput = ({ onSendMessage }) => {
  const [input, setInput] = useState("");
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input);
      setInput("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 relative">
      <textarea
        ref={textareaRef}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        className="w-full p-3 pr-14 border rounded-lg bg-gray-700 text-white border-gray-600 resize-none overflow-hidden focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Message TARS"
        rows={1}
      />
      <button
        type="submit"
        className="absolute right-3 bottom-3 bg-blue-500 text-white p-1.5 rounded-full hover:bg-blue-600 transition-colors duration-200 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-blue-300"
      >
        <Send size={16} />
      </button>
    </form>
  );
};

const TerminalControls = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleNewInstance = () => {
    console.log("New Instance button clicked");
  };

  const handleLoadInstance = (instanceId) => {
    console.log("Load Instance clicked", instanceId);
  };

  return (
    <div className="flex w-full mb-2">
      <button
        onClick={handleNewInstance}
        className="flex-1 bg-blue-500 text-white p-2 rounded-l-lg hover:bg-blue-600 transition-colors duration-200 flex items-center justify-center"
      >
        <RefreshCw size={16} className="mr-1" />
        New Instance
      </button>
      <div className="relative flex-1">
        <button
          onClick={() => setIsDropdownOpen(!isDropdownOpen)}
          className="w-full bg-gray-700 text-white p-2 rounded-r-lg hover:bg-gray-600 transition-colors duration-200 flex items-center justify-center"
        >
          <ChevronDown size={16} className="mr-1" />
          Load Instance
        </button>
        {isDropdownOpen && (
          <div className="absolute z-10 mt-1 w-full rounded-md shadow-lg bg-gray-700 ring-1 ring-black ring-opacity-5">
            <div
              className="py-1"
              role="menu"
              aria-orientation="vertical"
              aria-labelledby="options-menu"
            >
              {["Instance 1", "Instance 2", "Instance 3"].map(
                (instance, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      handleLoadInstance(index);
                      setIsDropdownOpen(false);
                    }}
                    className="block w-full text-left px-4 py-2 text-sm text-white hover:bg-gray-600"
                    role="menuitem"
                  >
                    {instance}
                  </button>
                ),
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export const TerminalOutput = React.forwardRef(({ output }, ref) => (
  <pre
    ref={ref}
    className="bg-black text-green-500 p-4 flex-grow overflow-auto font-mono rounded"
    style={{
      scrollbarWidth: "none",
      msOverflowStyle: "none",
      "&::-webkit-scrollbar": {
        display: "none",
      },
    }}
  >
    {output}
  </pre>
));

export const ChatMessage = ({ message, isUser, isStreaming }) => {
  const markdownComponents = {
    code({ node, inline, className, children, ...props }) {
      const match = /language-(\w+)/.exec(className || "");
      return !inline && match ? (
        <SyntaxHighlighter
          style={vscDarkPlus}
          language={match[1]}
          PreTag="div"
          {...props}
        >
          {String(children).replace(/\n$/, "")}
        </SyntaxHighlighter>
      ) : (
        <code className={`${className} bg-gray-800 rounded px-1`} {...props}>
          {children}
        </code>
      );
    },
    p: ({ children }) => <p style={{ marginBottom: "4px" }}>{children}</p>,
    ul: ({ children }) => (
      <ul
        style={{
          listStyleType: "disc",
          paddingLeft: "16px",
          marginBottom: "4px",
        }}
      >
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol
        style={{
          listStyleType: "decimal",
          paddingLeft: "16px",
          marginBottom: "4px",
        }}
      >
        {children}
      </ol>
    ),
    li: ({ children }) => <li style={{ marginBottom: "2px" }}>{children}</li>,
    a: ({ href, children }) => (
      <a
        href={href}
        style={{ color: "#60a5fa", textDecoration: "underline" }}
        target="_blank"
        rel="noopener noreferrer"
      >
        {children}
      </a>
    ),
    blockquote: ({ children }) => (
      <blockquote
        style={{
          borderLeft: "4px solid #9ca3af",
          paddingLeft: "16px",
          fontStyle: "italic",
          margin: "4px 0",
        }}
      >
        {children}
      </blockquote>
    ),
    img: ({ src, alt }) => (
      <img
        src={src}
        alt={alt}
        style={{
          maxWidth: "100%",
          height: "auto",
          margin: "4px 0",
          borderRadius: "8px",
        }}
      />
    ),
    table: ({ children }) => (
      <div style={{ overflowX: "auto" }}>
        <table
          style={{
            width: "auto",
            borderCollapse: "collapse",
            margin: "4px 0",
          }}
        >
          {children}
        </table>
      </div>
    ),
    th: ({ children }) => (
      <th
        style={{
          border: "1px solid #4b5563",
          padding: "4px",
          backgroundColor: "#1f2937",
        }}
      >
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td style={{ border: "1px solid #4b5563", padding: "4px" }}>
        {children}
      </td>
    ),
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
      <div
        style={{
          maxWidth: "90%",
          width: "auto",
          backgroundColor: isUser ? "#3b82f6" : "#374151",
          color: isUser ? "white" : "#e5e7eb",
          padding: "10px 14px",
          borderRadius: "12px",
          overflow: "auto",
          wordWrap: "break-word",
          lineHeight: "1.5",
          boxSizing: "border-box",
        }}
      >
        <div className="overflow-x-auto">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={markdownComponents}
            className="markdown-body break-words"
          >
            {message}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

const useSmartTooltip = () => {
  const [tooltipStyle, setTooltipStyle] = useState({});
  const buttonRef = useRef(null);
  const tooltipRef = useRef(null);

  useEffect(() => {
    const updateTooltipPosition = () => {
      if (buttonRef.current && tooltipRef.current) {
        const button = buttonRef.current.getBoundingClientRect();
        const tooltip = tooltipRef.current.getBoundingClientRect();
        const container = buttonRef.current
          .closest(".chat-interface")
          .getBoundingClientRect();

        let left = button.left + button.width / 2 - tooltip.width / 2;
        let top = button.top - tooltip.height - 8;

        // Ensure tooltip doesn't exceed container boundaries
        if (left < container.left) {
          left = container.left;
        } else if (left + tooltip.width > container.right) {
          left = container.right - tooltip.width;
        }

        // Adjust vertical position if tooltip goes above the container
        if (top < container.top) {
          top = button.bottom + 8;
        }

        setTooltipStyle({
          left: `${left}px`,
          top: `${top}px`,
          maxWidth: `${container.width * 0.8}px`, // Limit tooltip width
        });
      }
    };

    window.addEventListener("resize", updateTooltipPosition);
    updateTooltipPosition();

    return () => window.removeEventListener("resize", updateTooltipPosition);
  }, []);

  return { buttonRef, tooltipRef, tooltipStyle };
};

const PromptButton = ({ icon: Icon, prompt, onClick }) => {
  const { buttonRef, tooltipRef, tooltipStyle } = useSmartTooltip();

  return (
    <div className="w-full h-full">
      <button
        ref={buttonRef}
        onClick={() => onClick(prompt)}
        className="w-full h-full bg-gray-700 rounded-lg flex items-center justify-center hover:bg-gray-600 transition-colors duration-200 group relative p-2" // Added padding
      >
        <Icon size={18} className="text-white" />{" "}
        {/* Slightly increased icon size */}
        <span
          ref={tooltipRef}
          className="fixed bg-gray-800 text-white text-xs rounded py-1 px-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-normal z-10 pointer-events-none"
          style={tooltipStyle}
        >
          {prompt}
        </span>
      </button>
    </div>
  );
};

export const ChatInterface = ({
  handleSendMessage,
  messages,
  isLoading,
  terminalOutput,
  streamingMessage,
}) => {
  const messagesEndRef = useRef(null);
  const terminalEndRef = useRef(null);
  const [showSuggestedPrompts, setShowSuggestedPrompts] = useState(true);

  const suggestedPrompts = [
    { icon: Code, prompt: "Explain React hooks" },
    { icon: Zap, prompt: "Optimize React performance" },
    { icon: Layout, prompt: "Explain CSS Grid" },
    { icon: Globe, prompt: "What's new in ES2021?" },
    { icon: Server, prompt: "RESTful API principles" },
    { icon: Database, prompt: "SQL vs NoSQL databases" },
    { icon: Lock, prompt: "Web security best practices" },
    { icon: Smartphone, prompt: "Intro to React Native" },
    { icon: Cloud, prompt: "Cloud computing basics" },
    { icon: GitBranch, prompt: "Git workflow best practices" },
    { icon: Cpu, prompt: "Machine learning basics" },
    { icon: Terminal, prompt: "Useful Linux commands" },
    { icon: Box, prompt: "Intro to Docker containers" },
    { icon: Webhook, prompt: "What are webhooks?" },
    { icon: Fingerprint, prompt: "Authentication methods" },
    { icon: Network, prompt: "Computer networking basics" },
    { icon: Binary, prompt: "Binary search algorithm" },
    { icon: Layers, prompt: "Software architecture patterns" },
    { icon: Gauge, prompt: "Web app performance tips" },
    { icon: Bug, prompt: "Common debugging techniques" },
    { icon: GitCommit, prompt: "Explain CI/CD pipelines" },
    { icon: Code, prompt: "Statistical concepts in programming" },
    { icon: FileJson, prompt: "Working with JSON data" },
    { icon: Puzzle, prompt: "Explain dependency injection" },
    { icon: Lightbulb, prompt: "Tips for writing clean code" },
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingMessage]);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [terminalOutput]);

  useEffect(() => {
    setShowSuggestedPrompts(messages.length === 0);
  }, [messages]);

  const handleSuggestedPrompt = (prompt) => {
    handleSendMessage(prompt);
    setShowSuggestedPrompts(false);
  };

  const hideScrollbarStyle = {
    scrollbarWidth: "none",
    msOverflowStyle: "none",
    "&::-webkit-scrollbar": {
      display: "none",
    },
  };

  return (
    <div className="flex h-full">
      <div className="w-1/2 p-2 flex flex-col border-r border-gray-700 chat-interface">
        <h2 className="text-xl font-bold mb-2 flex items-center">
          <MessageSquare className="mr-2" /> Chat
        </h2>
        <div
          className="flex-grow overflow-y-auto mb-2"
          style={hideScrollbarStyle}
        >
          {showSuggestedPrompts ? (
            <div
              className="h-full flex items-start justify-center p-2 overflow-y-auto"
              style={hideScrollbarStyle}
            >
              <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 xl:grid-cols-8 gap-3 w-full max-w-4xl">
                {suggestedPrompts.map((item, index) => (
                  <div key={index} className="aspect-w-1 aspect-h-1">
                    <PromptButton
                      icon={item.icon}
                      prompt={item.prompt}
                      onClick={handleSuggestedPrompt}
                    />
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              {messages.map((msg, index) => (
                <ChatMessage
                  key={index}
                  message={msg.text}
                  isUser={msg.isUser}
                />
              ))}
              {streamingMessage && (
                <ChatMessage
                  message={streamingMessage}
                  isUser={false}
                  isStreaming={true}
                />
              )}
              {isLoading && !streamingMessage && (
                <div className="text-center text-gray-400">Loading...</div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
        <ChatInput onSendMessage={handleSendMessage} />
      </div>
      <div className="w-1/2 p-2 flex flex-col">
        <h2 className="text-xl font-bold mb-2 flex items-center">
          <Terminal className="mr-2" /> Terminal View
        </h2>
        <TerminalControls />
        <TerminalOutput ref={terminalEndRef} output={terminalOutput} />
      </div>
    </div>
  );
};

export default ChatInterface;
