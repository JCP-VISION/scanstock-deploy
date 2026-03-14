/**
 * ScanStock Documentation Scripts
 * Handles theme toggling, copy-to-clipboard, and navigation.
 */

// Theme Management - Enforced Dark Mode
const reflectPreference = () => {
    document.documentElement.setAttribute('data-theme', 'dark');
};

// Initialize Theme
reflectPreference();

// Code Copy Buttons
document.querySelectorAll("pre").forEach(block => {
    const button = document.createElement("button");
    button.className = "copy-btn";
    button.innerHTML = '<span>Copy</span>'; // Structure allows for CSS ::before icon

    button.onclick = () => {
        const codeText = block.querySelector("code") ? block.querySelector("code").innerText : block.innerText;
        navigator.clipboard.writeText(codeText.replace(/Copy$/, '').trim()).then(() => {
            button.querySelector('span').innerText = "Copied!";
            button.classList.add("copied");
            setTimeout(() => {
                button.querySelector('span').innerText = "Copy";
                button.classList.remove("copied");
            }, 2000);
        });
    };

    block.appendChild(button);
});

// Active Link Highlighting
const updateActiveLink = () => {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.sidebar nav a').forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
};

updateActiveLink();

// Mobile Menu Toggle (To be implemented if needed)
function toggleMobileMenu() {
    const nav = document.querySelector('.sidebar nav');
    nav.classList.toggle('open');
}