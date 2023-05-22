function submitForm() {
    var userInput = document.getElementById('userInput').value;
    console.log("Sending message: " + userInput);
    eel.send_message_to_gpt4(userInput)(function(result) {
        console.log("Received result: " + result);
        displayResult(result);
    });
}

function displayResult(result) {
    console.log("Displaying result: " + result);
    var resultDiv = document.getElementById('result');
    resultDiv.innerHTML = result;
}
