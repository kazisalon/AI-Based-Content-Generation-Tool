<!-- App.vue -->
<template>
	<div class="flex h-screen bg-gradient-to-b from-gray-900 to-gray-800">
		<!-- Sidebar -->
		<nav
			class="w-80 bg-gray-800/95 backdrop-blur-sm flex flex-col shadow-xl transform transition-transform duration-300 ease-in-out"
			:class="{ '-translate-x-80': isSidebarCollapsed }"
		>
			<!-- New Chat Button -->
			<button
				class="mx-4 my-6 p-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition-all flex items-center gap-3 font-medium shadow-lg hover:shadow-blue-500/20"
				@click="startNewChat"
			>
				<svg
					class="w-5 h-5"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						strokeLinecap="round"
						strokeLinejoin="round"
						strokeWidth="2"
						d="M12 4v16m8-8H4"
					></path>
				</svg>
				New Chat
			</button>

			<!-- Chat History -->
			<div class="flex-1 overflow-y-auto custom-scrollbar px-3">
				<div
					v-for="(chat, index) in chatHistory"
					:key="index"
					class="group relative p-4 mb-2 rounded-xl cursor-pointer flex items-center gap-3 transition-all"
					:class="{
						'bg-gray-700 shadow-md': currentChatIndex === index,

						'hover:bg-gray-700/50': currentChatIndex !== index,
					}"
					@click="switchChat(index)"
				>
					<svg
						class="w-5 h-5 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							strokeLinecap="round"
							strokeLinejoin="round"
							strokeWidth="2"
							d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
						></path>
					</svg>
					<span class="flex-1 truncate text-gray-200 font-medium">
						{{ chat.title || "New Chat" }}
					</span>
					<button
						class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-400 transition-all"
						@click.stop="deleteChat(index)"
					>
						<svg
							class="w-5 h-5"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								strokeLinecap="round"
								strokeLinejoin="round"
								strokeWidth="2"
								d="M6 18L18 6M6 6l12 12"
							></path>
						</svg>
					</button>
				</div>
			</div>

			<!-- Bottom Section -->
			<div class="p-4 border-t border-gray-700/50">
				<button
					class="w-full p-4 mb-4 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-xl transition-all flex items-center justify-center gap-3 font-medium"
					@click="clearHistory"
				>
					<svg
						class="w-5 h-5"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							strokeLinecap="round"
							strokeLinejoin="round"
							strokeWidth="2"
							d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
						></path>
					</svg>
					Clear History
				</button>
				<div class="flex items-center gap-3 p-4 rounded-xl bg-gray-700/50">
					<svg
						class="w-6 h-6 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							strokeLinecap="round"
							strokeLinejoin="round"
							strokeWidth="2"
							d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
						></path>
					</svg>
					<span class="text-gray-300 font-medium">User Account</span>
				</div>
			</div>
		</nav>

		<!-- Main Content -->
		<main class="flex-1 flex flex-col relative">
			<!-- Toggle Sidebar Button -->
			<button
				class="absolute top-6 left-6 z-10 p-2 text-gray-400 hover:text-white transition-colors bg-gray-800/80 rounded-lg backdrop-blur-sm"
				@click="toggleSidebar"
			>
				<svg
					class="w-6 h-6"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						strokeLinecap="round"
						strokeLinejoin="round"
						strokeWidth="2"
						d="M4 6h16M4 12h16M4 18h16"
					></path>
				</svg>
			</button>

			<!-- Chat Container -->
			<div
				class="flex-1 overflow-y-auto custom-scrollbar p-4 pt-20"
				ref="chatContainer"
			>
				<!-- Empty State -->
				<div
					v-if="currentChat.messages.length === 0"
					class="h-full flex flex-col items-center justify-center text-center px-4"
				>
					<div class="max-w-2xl">
						<h1
							class="text-5xl font-bold text-white mb-6 bg-gradient-to-r from-blue-500 to-emerald-500 bg-clip-text text-transparent"
						>
							Welcome to AI Chat
						</h1>
						<p class="text-gray-400 text-xl mb-12">
							Start a conversation by typing your message below. Ask questions,
							get answers, and explore ideas together.
						</p>
						<div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
							<div
								class="p-6 rounded-xl bg-gray-800/50 border border-gray-700/50 backdrop-blur-sm shadow-lg"
							>
								<h3 class="font-medium text-white text-lg mb-4">Examples</h3>
								<p class="text-gray-400 mb-2">"Explain quantum computing"</p>
								<p class="text-gray-400">"Write a poem about spring"</p>
							</div>
							<div
								class="p-6 rounded-xl bg-gray-800/50 border border-gray-700/50 backdrop-blur-sm shadow-lg"
							>
								<h3 class="font-medium text-white text-lg mb-4">
									Capabilities
								</h3>
								<p class="text-gray-400 mb-2">Remembers conversation context</p>
								<p class="text-gray-400">Provides detailed explanations</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Chat Messages -->
				<div v-else class="max-w-4xl mx-auto">
					<TransitionGroup name="message" appear>
						<div
							v-for="(message, index) in currentChat.messages"
							:key="index"
							class="message-wrapper mb-8"
						>
							<div
								class="message-bubble rounded-2xl p-6 shadow-lg"
								:class="[
									message.role === 'user'
										? 'bg-blue-600/10 border border-blue-500/20'
										: 'bg-gray-800/90 border border-gray-700/50',
								]"
							>
								<div class="flex gap-4 items-start">
									<div
										class="w-10 h-10 rounded-xl flex items-center justify-center shadow-lg"
										:class="
											message.role === 'user' ? 'bg-blue-600' : 'bg-emerald-600'
										"
									>
										<span class="text-white text-lg">
											{{ message.role === "user" ? "👤" : "🤖" }}
										</span>
									</div>
									<div
										class="flex-1 min-w-0 prose prose-invert prose-lg max-w-none"
									>
										<div
											v-if="message.role === 'assistant'"
											v-html="renderMarkdown(message.content)"
										></div>
										<div v-else class="text-white">{{ message.content }}</div>
									</div>
								</div>
							</div>
						</div>
					</TransitionGroup>
				</div>

				<!-- Loading Indicator -->
				<div v-if="loading" class="max-w-4xl mx-auto">
					<div
						class="message-bubble rounded-2xl p-6 bg-gray-800/90 border border-gray-700/50 shadow-lg"
					>
						<div class="flex gap-4 items-center">
							<div
								class="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center shadow-lg"
							>
								<span class="text-white text-lg">🤖</span>
							</div>
							<div class="typing-indicator">
								<div class="typing-dot"></div>
								<div class="typing-dot"></div>
								<div class="typing-dot"></div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Input Section -->
			<div
				class="p-6 border-t border-gray-700/50 bg-gray-800/95 backdrop-blur-sm"
			>
				<form @submit.prevent="sendMessage" class="max-w-4xl mx-auto relative">
					<div class="relative">
						<textarea
							v-model="userInput"
							@keydown.enter.prevent="handleEnterPress"
							@input="autoResize"
							ref="inputTextarea"
							placeholder="Type your message here..."
							rows="1"
							class="w-full bg-gray-700/50 text-white rounded-xl pl-6 pr-16 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-none max-h-[200px] custom-scrollbar text-lg backdrop-blur-sm"
						></textarea>
						<button
							type="submit"
							class="absolute right-3 bottom-3 p-2 text-white rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
							:class="
								userInput.trim() && !loading
									? 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
									: 'bg-gray-600'
							"
							:disabled="!userInput.trim() || loading"
						>
							<svg
								class="w-6 h-6"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									strokeLinecap="round"
									strokeLinejoin="round"
									strokeWidth="2"
									d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
								></path>
							</svg>
						</button>
					</div>
					<div class="mt-3 text-center text-gray-500 text-sm">
						Press Enter to send, Shift + Enter for new line
					</div>
				</form>
			</div>
		</main>
	</div>
</template>

<script>
import { marked } from "marked";
import DOMPurify from "dompurify";
import hljs from "highlight.js";
import "highlight.js/styles/nord.css";

export default {
	name: "App",
	data() {
		return {
			isSidebarCollapsed: false,
			userInput: "",
			loading: false,
			chatHistory: [
				{
					title: "",
					messages: [],
				},
			],
			currentChatIndex: 0,
		};
	},

	computed: {
		currentChat() {
			return this.chatHistory[this.currentChatIndex];
		},
	},

	created() {
		// Configure marked options
		marked.setOptions({
			highlight: function (code, lang) {
				if (lang && hljs.getLanguage(lang)) {
					return hljs.highlight(code, {
						language: lang,
					}).value;
				}
				return hljs.highlightAuto(code).value;
			},
			breaks: true,
			gfm: true,
		});

		// Load chat history from localStorage
		const savedHistory = localStorage.getItem("chatHistory");
		if (savedHistory) {
			try {
				this.chatHistory = JSON.parse(savedHistory);
			} catch (e) {
				console.error("Failed to load chat history:", e);
				localStorage.removeItem("chatHistory");
			}
		}
	},

	watch: {
		chatHistory: {
			deep: true,
			handler(newValue) {
				// Save to localStorage whenever chat history changes
				localStorage.setItem("chatHistory", JSON.stringify(newValue));
			},
		},
	},

	methods: {
		renderMarkdown(content) {
			try {
				const html = marked(content);
				return DOMPurify.sanitize(html);
			} catch (e) {
				console.error("Markdown rendering error:", e);
				return content;
			}
		},

		toggleSidebar() {
			this.isSidebarCollapsed = !this.isSidebarCollapsed;
		},

		startNewChat() {
			this.chatHistory.unshift({
				title: "",
				messages: [],
			});
			this.currentChatIndex = 0;
			this.userInput = "";
		},

		switchChat(index) {
			this.currentChatIndex = index;
			this.$nextTick(() => {
				this.scrollToBottom();
			});
		},

		deleteChat(index) {
			if (confirm("Are you sure you want to delete this chat?")) {
				this.chatHistory = this.chatHistory.filter((_, i) => i !== index);
				if (this.currentChatIndex >= this.chatHistory.length) {
					this.currentChatIndex = this.chatHistory.length - 1;
				}
				if (this.chatHistory.length === 0) {
					this.startNewChat();
				}
			}
		},

		clearHistory() {
			if (
				confirm(
					"Are you sure you want to clear all chats? This cannot be undone."
				)
			) {
				this.chatHistory = [
					{
						title: "",
						messages: [],
					},
				];
				this.currentChatIndex = 0;
				localStorage.removeItem("chatHistory");
			}
		},

		handleEnterPress(e) {
			if (!e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
				e.preventDefault();
				this.sendMessage();
			}
		},

		autoResize() {
			const textarea = this.$refs.inputTextarea;
			textarea.style.height = "auto";
			textarea.style.height = textarea.scrollHeight + "px";
		},

		scrollToBottom() {
			this.$nextTick(() => {
				const container = this.$refs.chatContainer;
				if (container) {
					container.scrollTop = container.scrollHeight;
				}
			});
		},

		async saveContent(content, contentType) {
			try {
				const response = await fetch("http://localhost:5000/save", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						content: content,
						content_type: contentType,
					}),
				});

				if (!response.ok) {
					throw new Error("Failed to save content");
				}

				const data = await response.json();
				return data.filename;
			} catch (error) {
				console.error("Error saving content:", error);
				return null;
			}
		},

		async sendMessage() {
			if (!this.userInput.trim() || this.loading) return;

			const message = this.userInput.trim();
			this.userInput = "";
			this.$refs.inputTextarea.style.height = "auto";

			// Add user message
			this.currentChat.messages.push({
				role: "user",
				content: message,
			});

			// Set chat title if it's the first message
			if (this.currentChat.messages.length === 1) {
				this.currentChat.title =
					message.slice(0, 30) + (message.length > 30 ? "..." : "");
			}

			this.loading = true;
			this.scrollToBottom();

			try {
				const response = await fetch("http://localhost:5000/generate", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						content_type: "1", // Using blog post type as default
						topic: message,
					}),
				});

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				const data = await response.json();

				if (data.error) {
					throw new Error(data.error);
				}

				if (data.content) {
					// Add assistant's response
					this.currentChat.messages.push({
						role: "assistant",
						content: data.content,
					});

					// Optionally save the content
					await this.saveContent(data.content, "1");
				} else {
					throw new Error("Invalid response format");
				}
			} catch (error) {
				console.error("Error details:", error);
				this.currentChat.messages.push({
					role: "assistant",
					content: `I encountered an error: ${error.message}. Please try again or check if the server is running.`,
				});
			} finally {
				this.loading = false;
				this.scrollToBottom();
			}
		},
	},
};
</script>

<style>
/* Custom scrollbar */
.custom-scrollbar::-webkit-scrollbar {
	width: 8px;
	height: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
	background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
	background-color: rgba(156, 163, 175, 0.3);
	border-radius: 20px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
	background-color: rgba(156, 163, 175, 0.5);
}

/* Message transitions */
.message-enter-active,
.message-leave-active {
	transition: all 0.3s ease;
}

.message-enter-from {
	opacity: 0;
	transform: translateY(20px);
}

.message-leave-to {
	opacity: 0;
	transform: translateY(-20px);
}

/* Typing indicator animation */
.typing-indicator {
	display: flex;
	gap: 4px;
	padding: 4px 8px;
	background: rgba(107, 114, 128, 0.3);
	border-radius: 12px;
}

.typing-dot {
	width: 8px;
	height: 8px;
	background-color: #ffffff;
	border-radius: 50%;
	animation: typing 1s infinite ease-in-out;
}

@keyframes typing {
	0%,
	100% {
		transform: translateY(0);
		opacity: 0.3;
	}

	50% {
		transform: translateY(-4px);
		opacity: 1;
	}
}

/* Markdown styling */
.prose pre {
	background: rgba(30, 41, 59, 0.5) !important;
	border: 1px solid rgba(71, 85, 105, 0.3) !important;
	border-radius: 8px !important;
	padding: 1rem !important;
	margin: 1rem 0 !important;
}

.prose code {
	background: rgba(30, 41, 59, 0.5) !important;
	color: #e2e8f0 !important;
	padding: 0.2em 0.4em !important;
	border-radius: 4px !important;
	font-size: 0.9em !important;
}

.prose pre code {
	background: transparent !important;
	padding: 0 !important;
	border-radius: 0 !important;
}

.prose {
	color: #e2e8f0 !important;
}

.prose a {
	color: #60a5fa !important;
	text-decoration: none !important;
}

.prose a:hover {
	text-decoration: underline !important;
}

.prose blockquote {
	border-left-color: #4b5563 !important;
	background: rgba(71, 85, 105, 0.2) !important;
	border-radius: 4px !important;
	padding: 1rem !important;
	margin: 1rem 0 !important;
}

.prose ul {
	list-style-type: disc !important;
	padding-left: 1.5rem !important;
}

.prose ol {
	list-style-type: decimal !important;
	padding-left: 1.5rem !important;
}

.prose h1,
.prose h2,
.prose h3,
.prose h4 {
	color: #f1f5f9 !important;
	margin-top: 1.5em !important;
	margin-bottom: 0.75em !important;
}

.prose table {
	width: 100% !important;
	border-collapse: collapse !important;
	margin: 1rem 0 !important;
}

.prose th,
.prose td {
	border: 1px solid rgba(71, 85, 105, 0.3) !important;
	padding: 0.75rem !important;
	text-align: left !important;
}

.prose th {
	background: rgba(30, 41, 59, 0.5) !important;
}

.prose hr {
	border-color: rgba(71, 85, 105, 0.3) !important;
	margin: 2rem 0 !important;
}
</style>
