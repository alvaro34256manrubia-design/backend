
const boton = document.getElementById('modoBtn');
const cuerpo = document.body;

if (localStorage.getItem('modo') === 'oscuro') {
  cuerpo.classList.add('dark');
}

boton.addEventListener('click', () => {
  cuerpo.classList.toggle('dark');

  if (cuerpo.classList.contains('dark')) {
    localStorage.setItem('modo', 'oscuro');
  } else {
    localStorage.setItem('modo', 'claro');
  }
});
