<!-- App.vue -->
<template>
	<div class="app">
		<!-- Sidebar -->
		<nav class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
			<!-- New Chat Button -->
			<button class="new-chat-btn" @click="startNewChat">
				<span class="plus-icon">+</span>
				New chat
			</button>

			<!-- History Section -->
			<div class="history-section">
				<div
					v-for="(chat, index) in chatHistory"
					:key="index"
					class="history-item"
					:class="{ active: currentChatIndex === index }"
					@click="switchChat(index)"
				>
					<span class="chat-icon">💭</span>
					<span class="chat-title">{{ chat.title || "New Chat" }}</span>
					<button class="delete-btn" @click.stop="deleteChat(index)">×</button>
				</div>
			</div>

			<!-- Bottom Section -->
			<div class="sidebar-bottom">
				<button class="clear-btn" @click="clearHistory">Clear all chats</button>
				<div class="user-section">
					<span class="user-icon">👤</span>
					<span>User Account</span>
				</div>
			</div>
		</nav>

		<!-- Main Content -->
		<main class="main-content">
			<!-- Toggle Sidebar Button -->
			<button class="toggle-sidebar" @click="toggleSidebar">☰</button>

			<!-- Chat Container -->
			<div class="chat-container" ref="chatContainer">
				<div v-if="currentChat.messages.length === 0" class="welcome-screen">
					<h1>AI Chat Assistant</h1>
					<p>Start a conversation by typing your message below</p>
				</div>

				<!-- Chat Messages -->
				<div v-else class="messages">
					<div
						v-for="(message, index) in currentChat.messages"
						:key="index"
						:class="['message', message.role]"
					>
						<div class="message-content">
							<span class="role-icon">{{
								message.role === "user" ? "👤" : "🤖"
							}}</span>
							<div class="message-text">{{ message.content }}</div>
						</div>
					</div>
				</div>

				<!-- Loading Indicator -->
				<div v-if="loading" class="loading-indicator">
					<div class="loading-dots">
						<span></span>
						<span></span>
						<span></span>
					</div>
				</div>
			</div>

			<!-- Input Section -->
			<div class="input-section">
				<form @submit.prevent="sendMessage" class="input-form">
					<div class="input-container">
						<textarea
							v-model="userInput"
							@keydown.enter.prevent="handleEnterPress"
							placeholder="Type your message here..."
							rows="1"
							ref="inputTextarea"
							@input="autoResize"
						></textarea>
						<button
							type="submit"
							class="send-btn"
							:disabled="!userInput.trim() || loading"
						>
							<span class="send-icon">↑</span>
						</button>
					</div>
					<div class="input-footer">
						Press Enter to send, Shift + Enter for new line
					</div>
				</form>
			</div>
		</main>
	</div>
</template>

<script>
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
	methods: {
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
		},
		deleteChat(index) {
			this.chatHistory = this.chatHistory.filter((_, i) => i !== index);
			if (this.currentChatIndex >= this.chatHistory.length) {
				this.currentChatIndex = this.chatHistory.length - 1;
			}
			if (this.chatHistory.length === 0) {
				this.startNewChat();
			}
		},
		clearHistory() {
			if (confirm("Are you sure you want to clear all chats?")) {
				this.chatHistory = [
					{
						title: "",
						messages: [],
					},
				];
				this.currentChatIndex = 0;
			}
		},
		handleEnterPress(e) {
			if (!e.shiftKey) {
				this.sendMessage();
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

			try {
				const response = await fetch("http://localhost:5000/generate", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						content_type: "1",
						topic: message,
					}),
				});

				const data = await response.json();

				if (!response.ok) {
					throw new Error(data.error || "Failed to generate response");
				}

				// Add AI response
				this.currentChat.messages.push({
					role: "assistant",
					content: data.content,
				});
			} catch (err) {
				this.currentChat.messages.push({
					role: "assistant",
					content: "Sorry, I encountered an error: " + err.message,
				});
			} finally {
				this.loading = false;
				this.$nextTick(() => {
					this.scrollToBottom();
				});
			}
		},
		autoResize(event) {
			const textarea = event.target;
			textarea.style.height = "auto";
			textarea.style.height = textarea.scrollHeight + "px";
		},
		scrollToBottom() {
			const container = this.$refs.chatContainer;
			if (container) {
				container.scrollTop = container.scrollHeight;
			}
		},
	},
	watch: {
		"currentChat.messages": {
			handler() {
				this.$nextTick(() => {
					this.scrollToBottom();
				});
			},
			deep: true,
		},
	},
	mounted() {
		window.addEventListener("resize", () => {
			if (window.innerWidth > 768) {
				this.isSidebarCollapsed = false;
			}
		});
	},
};
</script>

<style>
/* Reset and base styles */
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
}

html,
body {
	height: 100%;
	overflow: hidden;
}

body {
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
		Ubuntu, Cantarell, sans-serif;
	line-height: 1.5;
	background-color: #343541;
	color: #fff;
}

.app {
	display: flex;
	height: 100vh;
	width: 100vw;
}

/* Sidebar */
.sidebar {
	width: 260px;
	background-color: #202123;
	display: flex;
	flex-direction: column;
	transition: transform 0.3s ease;
	z-index: 1000;
}

.sidebar-collapsed {
	transform: translateX(-260px);
}

.new-chat-btn {
	margin: 8px;
	padding: 12px;
	background-color: #2d2d2f;
	border: 1px solid #4c4c4f;
	color: white;
	border-radius: 6px;
	cursor: pointer;
	display: flex;
	align-items: center;
	gap: 8px;
}

.history-section {
	flex: 1;
	overflow-y: auto;
	padding: 8px;
}

.history-item {
	padding: 10px;
	margin-bottom: 4px;
	border-radius: 6px;
	cursor: pointer;
	display: flex;
	align-items: center;
	gap: 8px;
}

.history-item:hover {
	background-color: #2d2d2f;
}

.history-item.active {
	background-color: #343541;
}

.chat-title {
	flex: 1;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.delete-btn {
	opacity: 0;
	background: none;
	border: none;
	color: #666;
	cursor: pointer;
}

.history-item:hover .delete-btn {
	opacity: 1;
}

.sidebar-bottom {
	padding: 8px;
	border-top: 1px solid #4c4c4f;
}

.clear-btn {
	width: 100%;
	padding: 10px;
	background-color: #2d2d2f;
	border: none;
	color: white;
	border-radius: 6px;
	cursor: pointer;
	margin-bottom: 8px;
}

.user-section {
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 10px;
	border-radius: 6px;
}

/* Main Content */
.main-content {
	flex: 1;
	display: flex;
	flex-direction: column;
	position: relative;
	background-color: #343541;
}

.toggle-sidebar {
	position: absolute;
	top: 12px;
	left: 12px;
	background: none;
	border: none;
	color: white;
	font-size: 24px;
	cursor: pointer;
	z-index: 10;
}

.chat-container {
	flex: 1;
	overflow-y: auto;
	padding: 20px;
	padding-top: 60px;
}

.welcome-screen {
	text-align: center;
	padding-top: 20vh;
}

.welcome-screen h1 {
	font-size: 2rem;
	margin-bottom: 1rem;
}

.messages {
	max-width: 800px;
	margin: 0 auto;
}

.message {
	padding: 20px;
	margin-bottom: 8px;
}

.message.assistant {
	background-color: #444654;
}

.message-content {
	display: flex;
	gap: 12px;
	align-items: flex-start;
}

.role-icon {
	font-size: 20px;
}

.message-text {
	flex: 1;
	line-height: 1.6;
}

/* Loading animation */
.loading-indicator {
	text-align: center;
	padding: 20px;
}

.loading-dots {
	display: flex;
	justify-content: center;
	gap: 8px;
}

.loading-dots span {
	width: 8px;
	height: 8px;
	background-color: #666;
	border-radius: 50%;
	animation: bounce 1s infinite;
}

.loading-dots span:nth-child(2) {
	animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
	animation-delay: 0.4s;
}

@keyframes bounce {
	0%,
	100% {
		transform: translateY(0);
	}

	50% {
		transform: translateY(-10px);
	}
}

/* Input section */
.input-section {
	padding: 16px;
	background-color: #343541;
	border-top: 1px solid #4c4c4f;
}

.input-form {
	max-width: 800px;
	margin: 0 auto;
}

.input-container {
	position: relative;
	background-color: #40414f;
	border-radius: 8px;
	padding: 12px;
}

textarea {
	width: 100%;
	background: none;
	border: none;
	color: white;
	font-size: 16px;
	resize: none;
	padding-right: 40px;
	max-height: 200px;
}

textarea:focus {
	outline: none;
}

.send-btn {
	position: absolute;
	right: 12px;
	bottom: 12px;
	background-color: #19c37d;
	border: none;
	color: white;
	width: 32px;
	height: 32px;
	border-radius: 6px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
}

.send-btn:disabled {
	background-color: #404041;
	cursor: not-allowed;
}

.input-footer {
	text-align: center;
	color: #666;
	font-size: 12px;
	margin-top: 8px;
}

/* Responsive styles */
@media (max-width: 768px) {
	.sidebar {
		position: absolute;
		height: 100%;
		top: 0;
		left: 0;
	}

	.main-content {
		width: 100%;
	}
}
</style>
