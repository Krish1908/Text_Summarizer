# AI Text Summarizer - HTML/CSS/JavaScript Frontend

A modern, beautiful, and responsive web interface for text summarization, inspired by the Tender_frontend React design but built with vanilla HTML, CSS, and JavaScript.

## 🎨 Features

### UI/UX Features
- **Modern Dark Theme**: Sleek dark interface with gradient accents and smooth animations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Smooth Animations**: CSS transitions and hover effects throughout
- **Scroll Animations**: Elements fade in as you scroll down the page
- **Fixed Navigation**: Sticky header with smooth scroll navigation

### Core Functionality
- **Real-time Statistics**: Character and word count as you type
- **Multiple Input Methods**: Text area, file upload, clipboard paste, sample text
- **Smart Configuration**: Model selection, temperature control, summary types, language selection
- **Export Options**: Copy to clipboard, download as text file
- **Keyboard Shortcuts**: Ctrl+Enter to summarize, Ctrl+K to clear, Ctrl+V to paste
- **Error Handling**: User-friendly error messages and success notifications

### Sections
1. **Hero Section**: Eye-catching landing with statistics and call-to-action
2. **Summarizer Interface**: Main text input and configuration panel
3. **Features Showcase**: Highlight key features with animated cards
4. **About Section**: Project information with AI visualization
5. **Footer**: Navigation and social links

## 🚀 Usage

### With FastAPI Backend (Recommended)
The frontend is now connected to your FastAPI backend:

1. **Start your FastAPI server** (from the APP directory):
   ```bash
   cd APP
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python main.py
   ```

2. **Open the frontend** in your browser:
   - Navigate to `http://localhost:8000` (if using the FastAPI server)
   - Or open `Text_Summarizer_UI/index.html` in a browser

3. **Use the application**:
   - Paste your text in the input area
   - Configure settings (model, temperature, summary type, language)
   - Click "Generate Summary" to process with your FastAPI backend
   - Use copy/download buttons to save your summary

### Standalone Demo
The frontend includes fallback simulation mode for testing without a backend:

1. Open `index.html` in any modern web browser
2. The interface will work with simulated responses
3. Perfect for testing UI/UX without backend dependencies

## 📁 Project Structure

```
Text_Summarizer_UI/
├── index.html          # Main HTML file with complete interface
├── styles.css          # Comprehensive CSS with modern design
├── script.js           # JavaScript functionality and logic
└── README.md           # This documentation file
```

## 🎨 Design Features

### Color Scheme
- **Primary**: Gradient from `#667eea` to `#7649e5`
- **Background**: Dark theme with `#0f172a` base
- **Text**: White and light gray for contrast
- **Accents**: Subtle shadows and borders

### Typography
- **System Font Stack**: Modern, readable fonts
- **Gradient Text**: Hero titles with gradient effects
- **Responsive Sizing**: Scales appropriately across devices

### Animations
- **Hover Effects**: Buttons and cards lift on hover
- **Transitions**: Smooth color and transform transitions
- **Loading States**: Animated spinner during processing
- **Scroll Effects**: Elements fade in as they enter viewport

## 🔧 Customization

### Colors
Edit CSS custom properties in `:root`:

```css
:root {
    --primary-color: #667eea;
    --text-color: #ffffff;
    --bg-color: #0f172a;
    /* ... more variables */
}
```

### Layout
The CSS uses CSS Grid and Flexbox for responsive layouts. Modify grid templates and flex properties to adjust spacing and alignment.

### Functionality
JavaScript is modular and well-commented. Add new features by extending the `TextSummarizer` class methods.

## 🌐 Browser Support

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **CSS Features**: Grid, Flexbox, Custom Properties, Animations
- **JavaScript Features**: ES6+ (Classes, Async/Await, Fetch API)
- **Mobile**: Full responsive support with touch-friendly interactions

## 📱 Responsive Breakpoints

- **Desktop**: 1024px and above
- **Tablet**: 768px - 1023px
- **Mobile**: Below 768px

## 🎯 Key Differences from React Version

1. **No Framework Dependencies**: Pure HTML/CSS/JS
2. **Built-in Simulation**: Works standalone without backend
3. **Simplified State Management**: Uses localStorage for configuration
4. **Direct DOM Manipulation**: No virtual DOM or complex state management
5. **Lighter Weight**: No build process or bundling required

## 🔗 Integration with Backend

To connect this frontend to your FastAPI backend:

1. **API Endpoint**: Ensure your backend has a `/api/summarize` endpoint
2. **CORS**: Configure CORS to allow requests from your frontend domain
3. **Authentication**: Add JWT tokens or API keys if required
4. **Response Format**: Match the expected JSON response structure

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- **Tender_frontend**: Inspiration for the design and layout
- **Font Awesome**: Icon library for beautiful icons
- **Modern CSS**: Grid, Flexbox, and custom properties for layout

---

**Made with ❤️ for modern web text summarization**