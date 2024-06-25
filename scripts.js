function toggleMobileMenu() {
  document.getElementById("menu").classList.toggle("active");
}

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  var scrollToTopBtn = document.getElementById("scrollToTopBtn");
  var scrollToBottomBtn = document.getElementById("scrollToBottomBtn");
  
  var documentHeight = document.documentElement.scrollHeight;
  var windowHeight = window.innerHeight;
  var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;

  // Show/Hide the "Scroll to Top" button
  if (scrollTop > 20) {
    scrollToTopBtn.style.display = "block";
  } else {
    scrollToTopBtn.style.display = "none";
  }

  // Show/Hide the "Scroll to Bottom" button
  if (scrollTop + windowHeight < documentHeight - 20) {
    scrollToBottomBtn.style.display = "block";
  } else {
    scrollToBottomBtn.style.display = "none";
  }
}

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

function scrollToNextSection() {
  const currentScroll = window.pageYOffset;
  const windowHeight = window.innerHeight;
  const documentHeight = document.documentElement.scrollHeight;

  // Scroll down one window height or to the bottom of the page
  const newScrollPosition = Math.min(currentScroll + windowHeight, documentHeight - windowHeight);
  
  window.scrollTo({
    top: newScrollPosition,
    behavior: 'smooth'
  });
}

// Add smooth scrolling to all links with the class 'nav-link'
document.querySelectorAll('.nav-link').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});

document.getElementById('user-input').addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
});

async function sendMessage() {
  const userInput = document.getElementById('user-input').value;
  if (!userInput) return;

  addMessageToChatLog('user', userInput);

  const response = await fetch('https://vast-castle-06901-6f6b60d7cd6b.herokuapp.com/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: userInput })
  });

  if (!response.ok) {
    console.error('Network response was not ok', response.statusText);
    return;
  }

  const data = await response.json();
  addMessageToChatLog('bot', data.response);

  document.getElementById('user-input').value = '';
}

function addMessageToChatLog(sender, message) {
  const chatLog = document.getElementById('chat-log');
  const newMessage = document.createElement('li');
  newMessage.innerHTML = `
    <span class="avatar ${sender}">${sender === 'bot' ? 'AI' : 'User'}</span>
    <div class="message">${message}</div>
  `;
  chatLog.appendChild(newMessage);
  chatLog.scrollTop = chatLog.scrollHeight;
}