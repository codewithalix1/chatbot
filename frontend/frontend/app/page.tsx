"use client";

import { FormEvent, useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

const suggestions = [
  "What fields can I update?",
  "Show me how user creation works",
  "What are the user management rules?",
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage(message?: string) {
    const text = (message ?? input).trim();

    if (!text || loading) return;

    setInput("");

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: text,
      },
    ]);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: text,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to communicate with the server");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.message,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the server. Please make sure the FastAPI backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    sendMessage();
  }

  return (
    <main className="min-h-screen bg-[#f7f7f5] text-[#171717]">
      <div className="flex min-h-screen">

        {/* Sidebar */}
        <aside className="hidden w-64 flex-col border-r border-black/5 bg-white px-5 py-6 md:flex">

          <div className="flex items-center gap-3 px-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-black text-sm font-semibold text-white">
              U
            </div>

            <div>
              <h1 className="text-sm font-semibold">UserAI</h1>
              <p className="text-xs text-black/40">Admin assistant</p>
            </div>
          </div>

          <button
            onClick={() => setMessages([])}
            className="mt-10 flex w-full items-center gap-3 rounded-xl bg-black px-4 py-3 text-sm font-medium text-white transition hover:bg-black/80"
          >
            <span className="text-lg">+</span>
            New conversation
          </button>

          <div className="mt-10">
            <p className="px-2 text-[11px] font-semibold uppercase tracking-wider text-black/35">
              Assistant
            </p>

            <div className="mt-3 rounded-xl bg-[#f5f5f3] px-3 py-3">
              <div className="flex items-center gap-3">
                <div className="h-2 w-2 rounded-full bg-green-500" />
                <div>
                  <p className="text-sm font-medium">Online</p>
                  <p className="text-xs text-black/40">
                    Ready to manage users
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-auto border-t border-black/5 pt-5">
            <div className="flex items-center gap-3 px-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#e9e9e6] text-xs font-semibold">
                A
              </div>

              <div>
                <p className="text-sm font-medium">Admin</p>
                <p className="text-xs text-black/40">Administrator</p>
              </div>
            </div>
          </div>
        </aside>

        {/* Main */}
        <section className="flex min-h-screen flex-1 flex-col">

          {/* Header */}
          <header className="flex h-16 items-center justify-between border-b border-black/5 bg-white/70 px-5 backdrop-blur md:px-8">
            <div>
              <p className="text-sm font-semibold">User Management</p>
              <p className="text-xs text-black/40">
                AI-powered administration
              </p>
            </div>

            <div className="flex items-center gap-2 rounded-full border border-black/5 bg-white px-3 py-1.5">
              <span className="h-2 w-2 rounded-full bg-green-500" />
              <span className="text-xs font-medium">Connected</span>
            </div>
          </header>

          {/* Chat */}
          <div className="flex flex-1 flex-col">

            <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col px-5 py-8 md:px-8">

              {messages.length === 0 ? (
                <div className="flex flex-1 flex-col items-center justify-center">

                  <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-black text-xl font-semibold text-white shadow-sm">
                    U
                  </div>

                  <h2 className="text-center text-3xl font-semibold tracking-tight md:text-4xl">
                    How can I help?
                  </h2>

                  <p className="mt-3 max-w-md text-center text-sm leading-6 text-black/45">
                    Manage users naturally. Ask me to add, update, search,
                    or remove users, or ask questions about the system.
                  </p>

                  <div className="mt-8 grid w-full max-w-xl gap-3 sm:grid-cols-3">
                    {suggestions.map((suggestion) => (
                      <button
                        key={suggestion}
                        onClick={() => sendMessage(suggestion)}
                        className="rounded-2xl border border-black/5 bg-white p-4 text-left text-xs leading-5 text-black/65 shadow-sm transition hover:-translate-y-0.5 hover:border-black/10 hover:shadow-md"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex flex-col gap-6 pb-8">

                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex ${
                        message.role === "user"
                          ? "justify-end"
                          : "justify-start"
                      }`}
                    >
                      <div
                        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-6 ${
                          message.role === "user"
                            ? "rounded-br-md bg-black text-white"
                            : "rounded-bl-md border border-black/5 bg-white text-black/75 shadow-sm"
                        }`}
                      >
                        {message.content}
                      </div>
                    </div>
                  ))}

                  {loading && (
                    <div className="flex justify-start">
                      <div className="rounded-2xl rounded-bl-md border border-black/5 bg-white px-5 py-4 shadow-sm">
                        <div className="flex gap-1.5">
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-black/30" />
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-black/30 [animation-delay:150ms]" />
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-black/30 [animation-delay:300ms]" />
                        </div>
                      </div>
                    </div>
                  )}

                </div>
              )}

            </div>

            {/* Input */}
            <div className="w-full border-t border-black/5 bg-white/70 px-5 py-5 backdrop-blur md:px-8">
              <form
                onSubmit={handleSubmit}
                className="mx-auto flex max-w-3xl items-center gap-3 rounded-2xl border border-black/10 bg-white p-2 shadow-sm focus-within:border-black/20 focus-within:shadow-md"
              >
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  disabled={loading}
                  placeholder="Ask me to add, update, search or remove a user..."
                  className="min-w-0 flex-1 bg-transparent px-3 py-2.5 text-sm outline-none placeholder:text-black/30 disabled:opacity-50"
                />

                <button
                  type="submit"
                  disabled={!input.trim() || loading}
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-black text-white transition hover:bg-black/80 disabled:cursor-not-allowed disabled:opacity-20"
                  aria-label="Send message"
                >
                  ↑
                </button>
              </form>

              <p className="mx-auto mt-2 max-w-3xl text-center text-[11px] text-black/30">
                AI assistant for authorized administrators
              </p>
            </div>

          </div>
        </section>
      </div>
    </main>
  );
}