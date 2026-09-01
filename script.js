const API = "http://localhost:5000"

async function askQuestion(){

let question = document.getElementById("question").value

let res = await fetch(API + "/ask", {
    method:"POST",
    headers:{
        "Content-Type":"application/json"
    },
    body: JSON.stringify({
        query: question
    })
})

let data = await res.json()

// ✅ Show AI answer
document.getElementById("answer").innerText = data.answer

// ✅ Show RAG results with score
let contextList = document.getElementById("context")
contextList.innerHTML = ""

if(data.results){
    data.results.forEach(item => {
        let li = document.createElement("li")
        li.innerText = item.text + " (Score: " + item.score + ")"
        contextList.appendChild(li)
    })
}

}


async function uploadFile(){

let file = document.getElementById("file").files[0]

let formData = new FormData()

formData.append("file",file)

let res = await fetch(API + "/upload",{

method:"POST",
body:formData

})

let data = await res.json()

let list = document.getElementById("analysis")

list.innerHTML=""

data.analysis.forEach(a=>{

let li = document.createElement("li")

li.innerText=a

list.appendChild(li)

})

}
async function generateFIR(){

let desc = document.getElementById("firInput").value

let res = await fetch("http://127.0.0.1:5000/generate-fir",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({description: desc})

})

let data = await res.json()

document.getElementById("firOutput").innerText = data.fir

}
async function summarize(){

let text = document.getElementById("inputText").value

let res = await fetch("http://127.0.0.1:5000/summarize",{

method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({text: text})

})

let data = await res.json()

document.getElementById("summary").innerText = data.summary

}
async function generateDraft(){

let prompt = document.getElementById("draftInput").value

let res = await fetch("http://127.0.0.1:5000/draft",{

method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({prompt: prompt})

})

let data = await res.json()

document.getElementById("draftOutput").innerText = data.draft

}
async function askLawyer(){

let question = document.getElementById("question").value

if(!question){
    alert("Enter question")
    return
}

let res = await fetch("http://127.0.0.1:5000/ai-lawyer",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
query: question
})

})

let data = await res.json()

if(data.error){
    document.getElementById("answer").innerText = data.error
}else{
    document.getElementById("answer").innerText = data.answer
}

}
async function getDecision(){

let query = document.getElementById("decisionInput").value

let res = await fetch("http://127.0.0.1:5000/legal-decision",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
query: query
})

})

let data = await res.json()

if(data.error){
    document.getElementById("decisionOutput").innerText = data.error
}else{
    document.getElementById("decisionOutput").innerText = data.decision
}

}
async function analyzeAI(){

let fileInput = document.getElementById("file").files[0]

let formData = new FormData()
formData.append("file", fileInput)

let res = await fetch("http://127.0.0.1:5000/analyze-ai", {
    method:"POST",
    body: formData
})

let data = await res.json()

document.getElementById("preview").innerText = data.preview
document.getElementById("output").innerText = data.analysis

}
async function askPDF() {
    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:5000/ask-pdf", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("pdfText").innerText = data.extracted_text;
    document.getElementById("pdfAnswer").innerText = data.answer;
}
