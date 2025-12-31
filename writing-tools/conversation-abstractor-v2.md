<PROMPT>

# 📝 Conversation Abstraction & Summarization Tool

## 🎯 **Objective**
You are tasked with abstracting and summarizing a conversation. Your goal is to provide a **clear, concise overview** of the exchange, highlighting key points and themes.

---

## 📥 **Input Data**

The conversation to analyze will be provided in the following format:

```xml
<conversation>
{{CONVERSATION}}
</conversation>
```

---

## 🔄 **Process Workflow**

### **Step 1:** 📖 Initial Review
Read through the entire conversation carefully.

### **Step 2:** 🔍 Exchange Identification  
Identify each distinct exchange between the participants.

### **Step 3:** ✍️ Exchange Processing
For each exchange, complete the following sub-tasks:

#### **3a.** 🏷️ **Title Creation**
- Create a brief, descriptive title
- Capture the main topic or purpose of the exchange
- Keep titles concise and meaningful

#### **3b.** 📄 **Summary Writing**
- Write a summary of **up to 125 words**
- For shorter exchanges, the summary can be proportionally shorter
- Maintain accuracy and completeness within word limits

### **Step 4:** 🎨 **Formatting & Presentation**
Format your output in a meaningful way that enhances readability and understanding. You may use:
- ✅ Headings
- ✅ Bullet points  
- ✅ Other formatting elements as appropriate

---

## 🎯 **Summary Focus Areas**

When writing your summaries, prioritize these elements:

| **Focus Area** | **Description** |
|---|---|
| **Main Ideas** | The core concepts or topics discussed |
| **Key Details** | Important specifics, examples, or supporting information |
| **Purpose/Outcome** | The intent behind the exchange and any resulting conclusions |

---

## 📤 **Output Format Requirements**

> **Important:** Your final output should consist **only** of the titled and summarized exchanges, formatted for clarity and ease of understanding. 
> 
> **Do not include** any additional commentary or analysis beyond the summaries themselves.

### **Required Structure:**

```xml
<answer>
[Title of Exchange 1]
[Summary of Exchange 1]

[Title of Exchange 2] 
[Summary of Exchange 2]

...and so on for each exchange in the conversation.
</answer>
```

---

## 🔧 **Quality Guidelines**

- ✅ **Clarity:** Ensure summaries are easily understood
- ✅ **Conciseness:** Stay within word limits while maintaining completeness  
- ✅ **Accuracy:** Faithfully represent the original conversation content
- ✅ **Structure:** Use consistent formatting throughout
- ✅ **Relevance:** Focus on the most important aspects of each exchange

</PROMPT>
