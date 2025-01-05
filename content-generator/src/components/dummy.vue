<!-- App.vue -->
<template>
	<div class="flex h-screen w-screen">
		<!-- Sidebar -->
		<nav
			class="w-64 bg-[#202123] flex flex-col transition-transform duration-300 z-[1000]"
			:class="{ '-translate-x-64': isSidebarCollapsed }"
		>
			<!-- New Chat Button -->
			<button
				class="m-2 p-3 bg-[#2d2d2f] border border-[#4c4c4f] text-white rounded-lg cursor-pointer flex items-center gap-2"
				@click="startNewChat"
			>
				<span class="plus-icon">+</span>
				New chat
			</button>

			<!-- History Section -->
			<div class="flex-1 overflow-y-auto p-2">
				<div
					v-for="(chat, index) in chatHistory"
					:key="index"
					class="p-2.5 mb-1 rounded-lg cursor-pointer flex items-center gap-2"
					:class="{
						'bg-[#343541]': currentChatIndex === index,
						'hover:bg-[#2d2d2f]': currentChatIndex !== index,
					}"
					@click="switchChat(index)"
				>
					<span class="text-xl">💭</span>
					<span class="flex-1 overflow-hidden text-ellipsis whitespace-nowrap">
						{{ chat.title || "New Chat" }}
					</span>
					<button
						class="text-gray-500 opacity-0 hover:opacity-100 group-hover:opacity-100"
						@click.stop="deleteChat(index)"
					>
						×
					</button>
				</div>
			</div>

			<!-- Bottom Section -->
			<div class="p-2 border-t border-[#4c4c4f]">
				<button
					class="w-full p-2.5 bg-[#2d2d2f] text-white rounded-lg cursor-pointer mb-2"
					@click="clearHistory"
				>
					Clear all chats
				</button>
				<div class="flex items-center gap-2 p-2.5 rounded-lg">
					<span class="text-xl">👤</span>
					<span>User Account</span>
				</div>
			</div>
		</nav>

		<!-- Main Content -->
		<main class="flex-1 flex flex-col relative bg-[#343541]">
			<!-- Toggle Sidebar Button -->
			<button
				class="absolute top-3 left-3 bg-transparent border-none text-white text-2xl cursor-pointer z-10"
				@click="toggleSidebar"
			>
				☰
			</button>

			<!-- Chat Container -->
			<div class="flex-1 overflow-y-auto p-5 pt-16" ref="chatContainer">
				<div
					v-if="currentChat.messages.length === 0"
					class="text-center pt-[20vh]"
				>
					<h1 class="text-4xl mb-4">AI Chat Assistant</h1>
					<p>Start a conversation by typing your message below</p>
				</div>

				<!-- Chat Messages -->
				<div v-else class="max-w-3xl mx-auto">
					<div
						v-for="(message, index) in currentChat.messages"
						:key="index"
						class="p-5 mb-2"
						:class="{ 'bg-[#444654]': message.role === 'assistant' }"
					>
						<div class="flex gap-3 items-start">
							<span class="text-xl">{{
								message.role === "user" ? "👤" : "🤖"
							}}</span>
							<div class="flex-1 leading-relaxed">{{ message.content }}</div>
						</div>
					</div>
				</div>

				<!-- Loading Indicator -->
				<div v-if="loading" class="text-center p-5">
					<div class="flex justify-center gap-2">
						<span
							v-for="i in 3"
							:key="i"
							class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
							:style="{ animationDelay: `${(i - 1) * 0.2}s` }"
						></span>
					</div>
				</div>
			</div>

			<!-- Input Section -->
			<div class="p-4 bg-[#343541] border-t border-[#4c4c4f]">
				<form @submit.prevent="sendMessage" class="max-w-3xl mx-auto">
					<div class="relative bg-[#40414f] rounded-lg p-3">
						<textarea
							v-model="userInput"
							@keydown.enter.prevent="handleEnterPress"
							placeholder="Type your message here..."
							rows="1"
							ref="inputTextarea"
							@input="autoResize"
							class="w-full bg-transparent border-none text-white text-base resize-none pr-10 max-h-[200px] focus:outline-none"
						></textarea>
						<button
							type="submit"
							class="absolute right-3 bottom-3 w-8 h-8 bg-[#19c37d] disabled:bg-[#404041] text-white rounded-lg cursor-pointer flex items-center justify-center disabled:cursor-not-allowed"
							:disabled="!userInput.trim() || loading"
						>
							<span>↑</span>
						</button>
					</div>
					<div class="text-center text-gray-500 text-xs mt-2">
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
