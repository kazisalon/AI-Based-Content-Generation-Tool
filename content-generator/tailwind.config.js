/** @type {import('tailwindcss').Config} */
export default {
	content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
	theme: {
		extend: {
			colors: {
				sidebar: "#202123",
				chatbg: "#343541",
				messagebg: "#444654",
				inputbg: "#40414f",
				border: "#4c4c4f",
				sendbtn: "#19c37d",
			},
		},
	},
	plugins: [],
};
