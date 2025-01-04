<!-- ContentGenerator.vue -->
<template>
	<div class="container">
		<h1>AI Content Generator</h1>

		<div class="card">
			<form @submit.prevent="generateContent" class="form">
				<div class="form-group">
					<label>Content Type</label>
					<select v-model="contentType">
						<option value="1">Blog Post</option>
						<option value="2">Social Media Post</option>
						<option value="3">Joke</option>
						<option value="4">Tutorial</option>
					</select>
				</div>

				<div class="form-group">
					<label>Topic</label>
					<input
						type="text"
						v-model="topic"
						placeholder="Enter your topic..."
						required
					/>
				</div>

				<button type="submit" :disabled="loading" class="button">
					<span v-if="loading" class="loader-container">
						<span class="loader"></span>
						Generating...
					</span>
					<span v-else>Generate Content</span>
				</button>
			</form>

			<div v-if="error" class="error">
				{{ error }}
			</div>

			<div v-if="generatedContent" class="content-section">
				<div class="content-header">
					<h2>Generated Content:</h2>
					<button @click="saveContent" class="save-button">Save Content</button>
				</div>
				<div class="generated-content">
					{{ generatedContent }}
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { ref } from "vue";

export default {
	name: "ContentGenerator",
	setup() {
		const contentType = ref("1");
		const topic = ref("");
		const generatedContent = ref("");
		const loading = ref(false);
		const error = ref("");

		const generateContent = async () => {
			loading.value = true;
			error.value = "";

			try {
				const response = await fetch("http://localhost:5000/generate", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						content_type: contentType.value,
						topic: topic.value,
					}),
				});

				const data = await response.json();

				if (!response.ok) {
					throw new Error(data.error || "Failed to generate content");
				}

				generatedContent.value = data.content;
			} catch (err) {
				error.value = err.message;
			} finally {
				loading.value = false;
			}
		};

		const saveContent = async () => {
			try {
				const response = await fetch("http://localhost:5000/save", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						content: generatedContent.value,
						content_type: contentType.value,
					}),
				});

				const data = await response.json();

				if (!response.ok) {
					throw new Error(data.error || "Failed to save content");
				}

				alert(`Content saved successfully to: ${data.filename}`);
			} catch (err) {
				error.value = err.message;
			}
		};

		return {
			contentType,
			topic,
			generatedContent,
			loading,
			error,
			generateContent,
			saveContent,
		};
	},
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background-color: #f5f5f5;
	padding: 2rem;
}

h1 {
	text-align: center;
	color: #333;
	font-size: 2rem;
	margin-bottom: 2rem;
}

.card {
	max-width: 800px;
	margin: 0 auto;
	background: white;
	padding: 2rem;
	border-radius: 8px;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form {
	display: flex;
	flex-direction: column;
	gap: 1.5rem;
}

.form-group {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

label {
	font-size: 0.875rem;
	font-weight: 600;
	color: #444;
}

input,
select {
	padding: 0.75rem;
	border: 1px solid #ddd;
	border-radius: 4px;
	font-size: 1rem;
}

input:focus,
select:focus {
	outline: none;
	border-color: #2563eb;
	box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}

.button {
	background-color: #2563eb;
	color: white;
	padding: 0.75rem;
	border: none;
	border-radius: 4px;
	font-size: 1rem;
	cursor: pointer;
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 0.5rem;
}

.button:hover {
	background-color: #1d4ed8;
}

.button:disabled {
	background-color: #93c5fd;
	cursor: not-allowed;
}

.loader-container {
	display: flex;
	align-items: center;
	gap: 0.5rem;
}

.loader {
	width: 20px;
	height: 20px;
	border: 3px solid #ffffff;
	border-radius: 50%;
	border-top-color: transparent;
	animation: spin 1s linear infinite;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

.error {
	margin-top: 1.5rem;
	padding: 1rem;
	background-color: #fee2e2;
	color: #dc2626;
	border-radius: 4px;
}

.content-section {
	margin-top: 1.5rem;
}

.content-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 1rem;
}

h2 {
	font-size: 1.25rem;
	font-weight: 600;
	color: #333;
}

.save-button {
	background-color: #059669;
	color: white;
	padding: 0.5rem 1rem;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}

.save-button:hover {
	background-color: #047857;
}

.generated-content {
	background-color: #f8fafc;
	padding: 1.5rem;
	border-radius: 4px;
	border: 1px solid #e2e8f0;
	white-space: pre-wrap;
	line-height: 1.6;
}
</style>
