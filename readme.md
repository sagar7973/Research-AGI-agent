# 🔍 Research AGI Assistant  
*A Chrome extension that automates web research using AI*

![Demo](docs/demo.gif)

## ✨ Features  
- Instantly summarize research queries  
- Cites sources from the web  
- FastAPI + OpenAI integration  

## 🛠️ Setup  
1. **Backend**:  
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Chrome Extension**:  
   - Go to `chrome://extensions`  
   - Enable "Developer mode"  
   - Click "Load unpacked" → Select `/extension` folder
   - You need your open API keys and paste it into .py file. 

  

## 📜 License  
MIT License - See [LICENSE](LICENSE)  