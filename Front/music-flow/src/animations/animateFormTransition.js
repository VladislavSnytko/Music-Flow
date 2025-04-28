import { gsap } from "gsap/dist/gsap";
import { Flip } from "gsap/dist/Flip";

gsap.registerPlugin(Flip);

export function animateFormTransition(currentEl, nextEl, onComplete) {
  if (!currentEl || !nextEl) return;

  // Подготовка элементов перед анимацией
  nextEl.style.display = 'block';
  nextEl.style.opacity = '0';
  nextEl.style.transform = 'translateY(20px)';
  
  // Сохраняем начальное состояние
  const state = Flip.getState([currentEl, nextEl], {
    props: "opacity, transform",
    simple: true
  });

  // Анимация исчезновения текущей формы
  gsap.to(currentEl, {
    opacity: 0,
    duration: 0.3,
    ease: "power2.in",
    onComplete: () => {
      currentEl.style.display = 'none';
    }
  });

  // Анимация появления новой формы с задержкой
  gsap.fromTo(nextEl, 
    { 
      opacity: 0,
      y: 30,
      scale: 0.98
    },
    {
      opacity: 1,
      y: 0,
      scale: 1,
      duration: 0.5,
      delay: 0.2,
      ease: "back.out(1.2)",
      onComplete: () => {
        onComplete?.();
      }
    }
  );

  // // Дополнительные эффекты для элементов формы
  // const inputs = nextEl.querySelectorAll('.auth-input');
  // gsap.from(inputs, {
  //   opacity: 0,
  //   y: 10,
  //   stagger: 0.05,
  //   duration: 0.3,
  //   delay: 0.4,
  //   ease: "power2.out"
  // });

  // const button = nextEl.querySelector('.form-button');
  // if (button) {
  //   gsap.from(button, {
  //     opacity: 0,
  //     y: 10,
  //     duration: 0.3,
  //     delay: 0.5,
  //     ease: "power2.out"
  //   });
  // }

  // const bottomText = nextEl.querySelector('.login-bottom-text');
  // if (bottomText) {
  //   gsap.from(bottomText, {
  //     opacity: 0,
  //     duration: 0.3,
  //     delay: 0.6,
  //     ease: "power2.out"
  //   });
  // }
}