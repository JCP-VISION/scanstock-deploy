function toggleTheme(){

  document.body.classList.toggle("dark")

}

document.querySelectorAll("pre").forEach(block=>{

  const button=document.createElement("button")
  button.innerText="Copy"

  button.onclick=()=>{

    navigator.clipboard.writeText(block.innerText)

    button.innerText="Copied!"

    setTimeout(()=>button.innerText="Copy",2000)

  }

  block.parentNode.insertBefore(button,block)

})