async function getapi(){
    const response = await fetch("http://127.0.0.1:8000");
    const data = await response.json();
    document.getElementById('result').textContent = `Course: ${data.Course} | ${data.Score}`;
}