import { gsap } from 'gsap'

export function animateFormTransition(container, currentEl, nextEl) {
  if (!container || !currentEl || !nextEl) return

  // 1) Засекаем стартовую высоту контейнера
  const startHeight = container.offsetHeight

  // 2) Подготовка «новой» карточки: сделать её видимой, но скрыть контент
  nextEl.style.position = 'absolute'
  nextEl.style.visibility = 'hidden'
  nextEl.style.display    = 'block'

  // 3) Засекаем конечную высоту контейнера
  const endHeight = nextEl.offsetHeight

  // 4) Восстанавливаем nextEl в нормальное состояние
  nextEl.style.position   = ''
  nextEl.style.visibility = ''
  nextEl.style.display    = ''

  // 5) Плавно анимируем высоту контейнера
  gsap.fromTo(container,
    { height: startHeight },
    { height: endHeight, duration: 0.5, ease: 'power1.inOut' }
  )

  // 6) Анимируем «исчезновение» старой карточки
  gsap.to(currentEl, {
    opacity: 0,
    duration: 0.3,
    ease: 'power2.in',
    onComplete: () => {
      currentEl.style.display = 'none'
    }
  })

  // 7) Анимируем «появление» новой карточки
  gsap.fromTo(nextEl,
    { opacity: 0, y: 20, scale: 0.98 },
    {
      opacity: 1,
      y: 0,
      scale: 1,
      duration: 0.4,
      delay: 0.3,
      ease: 'back.out(1.2)',
      onComplete: () => {
        // Сброс inline-стиля высоты, чтобы контейнер мог подстраиваться дальше
        container.style.height = 'auto'
      }
    }
  )
}
