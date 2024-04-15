const ProfileUpload = (event) => {
    const files = event.target.files;
    const filesLength = files.length;
    if (filesLength > 0) {
      const imageSrc = URL.createObjectURL(files[0]);
      const imagePreviewElement = document.querySelector(".Authentication-page .container .Section-2 form .tb-container .ProfilePhoto .image");
    //   imagePreviewElement.src = imageSrc;
    console.log(imageSrc);
      imagePreviewElement.style.backgroundImage = `url(${imageSrc})`;
    }
};
const CertificationUpload = (event) => {
    const files = event.target.files;
    const filesLength = files.length;
    if (filesLength > 0) {
      const imageSrc = URL.createObjectURL(files[0]);
      const imagePreviewElement = document.querySelector(".Authentication-page .container .Section-2 form .tb-container .Certification .image");
    //   imagePreviewElement.src = imageSrc;
    console.log(imageSrc);
      imagePreviewElement.style.backgroundImage = `url(${imageSrc})`;
    }
};

const data = {
  "Cairo": ["Nasr City", "Maadi", "Dokki"],
  "Alexandria": ["Al Ajmi", "Sidi Gaber", "El Muntaza"],
};

const governorateSelect = document.getElementById("governorate-select");

const regionSelect = document.getElementById("region-select");

function updateRegionOptions() {
  const selectedGovernorate = governorateSelect?.value;
  console.log(regionSelect);
  regionSelect.innerHTML = "<option value='' disabled selected>Chose Area</option>";
  if (selectedGovernorate && data[selectedGovernorate]) {
    data[selectedGovernorate].forEach(region => {
      const option = document.createElement("option");
      option.textContent = region;
      option.value = region;
      regionSelect.appendChild(option);
    });
  }
}

governorateSelect?.addEventListener("change", updateRegionOptions);

for (const governorate in data) {
  if (data.hasOwnProperty(governorate)) {
    const option = document.createElement("option");
    option.textContent = governorate;
    option.value = governorate;
    governorateSelect?.appendChild(option);
  }
}


/* Notification */
const notification = document.querySelector(".navbar .container .nav-item .Notification");
const bill = document.querySelector(".navbar .container .nav-item .BillFather");
const bgBill = document.querySelectorAll(".navbar .container .nav-item .BillFather .BillHover");

bill?.addEventListener("click", () => {
  notification.classList.toggle("show");
  bgBill.forEach((element) => {
    element.classList.toggle("BillColor");
  });
});

// Form Section
var answerQuestionOneElements = document.querySelectorAll('.formBody .form form .question1 .answers .answer');


answerQuestionOneElements.forEach(function(answerElement) {
    answerElement.addEventListener('click', function() {
      answer = answerElement.children[1].innerHTML
      document.getElementById("question1").value = answer
        answerQuestionOneElements.forEach(function(element) {
            element.querySelector('.formBody .form form .question1 .answers .answer .circle').classList.remove('choose');
          });
        answerElement.querySelector('.formBody .form form .question1 .answers .answer .circle').classList.toggle('choose');
      });
});

var answerQuestionTwoElements = document.querySelectorAll('.formBody .form form .question2 .answers .answer');

answerQuestionTwoElements.forEach(function(answerElement) {

    answerElement.addEventListener('click', function() {
      answer = answerElement.children[1].innerHTML
        document.getElementById("question2").value = answer
        answerQuestionTwoElements.forEach(function(element) {
            element.querySelector('.formBody .form form .question2 .answers .answer .circle').classList.remove('choose');
          });
        answerElement.querySelector('.formBody .form form .question2 .answers .answer .circle').classList.toggle('choose');
    });
});

// Rating Stars
const stars = document.querySelectorAll('.formBody .form form .question4 .answers .stars i');

stars.forEach((star, index) => {
  star.addEventListener('click', () => {
    toggleStars(index);
  });
});

function toggleStars(index) {
  for (let i = 0; i <= index; i++) {
    stars[i].classList.remove('fa-regular');
    stars[i].classList.add('fa-solid');
  }

  for (let i = index + 1; i < stars.length; i++) {
    stars[i].classList.remove('fa-solid');
    stars[i].classList.add('fa-regular');
  }
}

// Book Time
var timeElements = document.querySelectorAll('.doctorDetails .bookingInformation .reservationDate .days .day .time');

// Add click event listener to each 'time' element
timeElements.forEach(function(element) {
    element.addEventListener('click', function() {
        if (!element.classList.contains('booked')) {
          timeElements.forEach(function(el) {
            el.classList.remove('choose');
          });
          element.classList.add('choose');
          
          var allFooters = document.querySelectorAll('.doctorDetails .bookingInformation .reservationDate .days .day .footer');
          allFooters.forEach(function(footer) {
            footer.classList.remove('green');
          });
          
          var dayElement = element.closest('.day');
          if (dayElement) {
            var footerElement = dayElement.querySelector('.footer');
            if (footerElement) {
              footerElement.classList.add('green');
            }
          }
        }
          
    });
});

// Doctor Details Slider

var swiper = new Swiper('.swiper', {
  slidesPerView: 3,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    520: {
      slidesPerView: 3,
    },
    992:{
      slidesPerView: 2,
    },
    1200: {
      slidesPerView: 3,
    },
    // 1400:{
    //   slidesPerView: 4,
    // },
  },
});

// See More Comments
let seeMore = document.querySelector('#see-more');
let currentItem = 3;

seeMore.addEventListener('click', function() {
  let boxes = [...document.querySelectorAll('.doctorDetails .AllComments .comments .comment')];
  for (let i = currentItem; i < boxes.length ; i++) {
    boxes[i].style.display = 'flex';
  }
  seeMore.style.display = 'none';
})

// See More Time
let moreButtons = document.querySelectorAll('#more');

moreButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      let container = button.parentElement;
      let times = container.querySelectorAll('.time');

      times.forEach(function(time) {
          time.style.display = 'inline-block';
      });
      
      button.style.display = 'none';
    });
});

