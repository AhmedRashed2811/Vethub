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
    "Cairo": [
        "Nasr City", "Abbassia", "Ataba", "Ain Shams",
        "Al-Wayli", "Azbakeya", "Bab al-Louq", 
        "Downtown Cairo", "El Manial", "Bab El Khalq",
        "El Marg", "El Matareya", "El Qobbah", 
        "Ezbet El Nakhl", "Faggala", "Fifth Settlement","El Salam City", 
        "El Sayeda Zeinab", "Forth Settlement", "Third Settlement",
        "Second Settlement", "First Settlement", "New Cairo", "New Capital City", 
        "Fustat", "Garden City", "Heliopolis", "El-Shorouk City", "El-Zawya El-Hamra",
        "Manshiyat Naser", "Maadi", "New Maadi", "Old Cairo", 
        "Shubra", "Wagh El Birket", "El Sakkakini", 
        "Zeitoun", , "Masr Elgdida",
        "Almaza", "Alf Maskn", "Mo2tam" , "Al Basatin", "Kasr El Nile"],

    "Giza": [ 
        "Al Haram", "Al Remaya", 
        "Al Sefarat", "Al Warraq", "Ard El Golf",
        "Boulaq", "Dahab Island", "Dokki", "El Agouza",
        "El Haram", "El Mohandessin", "El Omrania", "El Sheikh Zayed", 
        "El Zamalek", "El-Bahr El A'azam", "Faisal",
        "Giza Square", "Hadayeq Al Ahram","Imbaba", "Kit Kat",
        "Konysa", "Nahia", "6th October City", "Hadayq October", "El Sheikh Zayed",
        "Atfyeh","Tersa", "Wadi El Nile"],

    "Alexandria" : [
        "Agami", "Anfoushi", "Bahary", 
        "Bacchus", "Bolkly", "Borg El Arab",
        "Cleopatra", "Dekhela", "El Azarita", 
        "El Bitash", "El Ibrahimeya", "El Labban", 
        "El Mansheya", "El Maqwa", "El Montaza", 
        "El Shatby", "El Thakafa", "El-Mandara", 
        "Gianaclis", "Glim", "Gomrok", "Hadara", 
        "Karmouz", "Koum Al Dikka", "Louran",
        "Miami", "Moharam Bek", "Moharram Bey", 
        "Montazah", "Mustafa Kamel", "Raml Station", 
        "Roushdy", "Safar", "Seyouf", "Sidi Bishr", 
        "Sidi Gaber", "Sidi Gaber El Nayoumy", "Smouha", 
        "Sporting", "Stanley", "Tosson", "Victor Emmanuel", 
        "Wabour El Maya"],

    "Al-Sharkia":[
        "Zagazig","10th of Ramadan City","Belbeis","Minya al-Qamh",
        "Al Ibrahimiyah","Al Qanayat","Abu Kabir","Al Qurayn","Fakous","New Salhia",
        "Abu Hammad","Kafr Saqr","Dairb Negm","Mashtul as-Souq","Hihya",
        "El Senbellawein","El Qantara Sharq","El Qantara Gharb",
        "El Manzala","Shibin El Qanater","El Husseinia","Olad Saqr","Zifta",
        "El Ibrahimiyah El Bahariya","El Qurainiya","El Obour"],
    
    "Al-Daqahlia": [
        "Al Mansurah","Al Mansurah Al Gadeeda","Al Matareya","Al Manzala","Talkha",
        "Meet Ghamr","Dikirnis","Belqas","Aga","Sherbin",
        "Meet Salsil","Nabroh","Bani Ubaid","El Senbellawein","Al Gamaliya",
        "Gharb Sannbelawain","Faraskour","Gamasa","Al Kurdi","Nubaria","Tamy Al Amdid"],

    "Al-Behyra":[
        "Damanhur","Kafr El Dawar","Rashid","Kom Hamada","Edko",
        "Abu al-Matamir","Abu Homs","Delengat","Mahmoudiyah","Rahmaniya",
        "Itai El Barud","Housh Eissa","Shubrakhit","Badr","Wadi Natrun",
        "Abu al-Nuwaris", "Hamoul","New Delengat","Bolk",
    ],

    "Al-Mania":[
        "Minya","Minya Al Gadeeda","Al-Mansha",
        "Samalut","Matay","Malawi","Bani Mazar",
        "Maghagha","El Adwa","Deir Mawas","Abu Qurqas",
        "Abu al-Matamir","Bani Adi","Al Fath","Al Badari",
    ],

    "Sohag":[
        "Sohag","Sohag Al Gadeeda","Akhmim",
        "Tama","Al Balina","Gerga","Dar As Salaam",
        "Al Maraghah","Al Khuwailidiyah","Qeft",
        "Saqilatah","Naqada","New Al Balina",
        "Al 'Asirat","Juhayna","Al Manshah","Salklata",
        "Naqous","Tahta","Tahmas","New Akhmim"
    ],

    "Al-Gharbia":[
      "Tanta","Tanta Al Gadeeda","Zefta","Kafr El Zayat",
      "Al Mahalla Al Kubra","Samanoud","Al Santa",
      "New Al Sennabra","Basyoun","Qutur","Al Taref",
    ],

    "Asyout": [
      "Assiut","Assiut Al Gadeeda","Abu Tig",
      "Al Qusiyya","Al Ghannayim","Dayrut","Dayrut Al Gadeeda",
      "Abu Tisahil","Al Manayat","Al Badari",
      "Sedfa","Abnub","Sahal Salim",
      "Abanob","Al Fath","Manfout"
    ],

    "Al-Menoufia": [
      "Shibin El Kom","Al Mahalla Al Kubra",
      "Al Bagour","El Shohadaa","Berket El Sabaa",
      "Tala","Al Sadat","Ashmun","Menouf",
      "Sers El-Lyan","Qweisna","Al Bagoura",
    ],

    "Fayoum": [
      "Fayoum","Fayoum Al Gadeeda","Tameya",
      "Snores","Abshway","AbshwayAl Gadeeda",
      "Etsa","Youssef El-Sedeeq","Nasriyah",
    ],

    "Kafr Al-Sheikh": [
      "Kafr El Sheikh", "Kafr El Sheikh Al Gadeeda",
      "Desouk","Metoubes","Bella","Fuwwah","El Riad",
      "Sidi Salem","Al Hamoul","Al Hamoul Al Gadeeda",
      "Baltim","Qaleen","Sidi Ghazi","El Burullus"
    ],
    
    "Qena":
    [
      "Qena","Qena Al Gadeeda","Abu Tesht",
      "Nagaa Hammadi","Naqada","Alwaqf","Deshna",
      "Qift","Quos","Al Wadi Al Jadid","Farshout",
    ],

    "Beni-Suef": [
      "Beni Suef","Beni Suef Al Gadeeda",
      "Al Wasta", "Biba","Fashn",
      "Naser","Ihnasia","Samasta",
    ],
    
    "Aswan": [
      "Aswan","Aswan Al Gadeeda","Kom Ombo",
      "Kom Ombo Al Gadeeda","Daraw", "Edfu",
    ],

    "Damietta": [
      "Damietta","Damietta Al Gadeeda","Ras El Bar",
      "Faraskur","Kafr Al Bateekh","Kafr Saad",
    ],

    "Ismailia":[
      "Ismailia","Ismailia Al Gadeeda",
      "Qantara Sharq","Qantara Gharb",
      "Fayed","Abu Sawir","Al Qassaseen",
    ],

    "Luxor": [
      "Luxor","Luxor Al Gadeeda","Abu El Nomros","Armant",
      "Al Toud","Al Bayadiyah","Al Qurnah",
      "Al Aayat","Al Bayadiyah Al Gadeeda",
      "Al Zainiyah","Al Shaghateen","Esna",
    ],

    "Port Said": [
      "Port Said","Port Fouad",
      "Port Tawfiq","Mobark","Al Afrang",
      "Al Manasra","Al Manakh","Al Manakh Al Jawi",
      "Al Manakh Al Jawi Al Gadeeda","Al Matari","Al Zohor",
      "Al Zohor Al Gadeeda","Al Arab","Al Dawahy"
    ], 

    "Suez": [
      "Suez","Suez Al Gadeeda","Al Jana'in",
      "Al Jana'in Al Gadeeda","Ataka","Faysel",
      "Al Arbaeen",
    ]
    


    

}

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
// const notification = document.querySelector(".navbar .container .nav-item .Notification");
// const bill = document.querySelector(".navbar .container .nav-item .BillFather");
// const bgBill = document.querySelectorAll(".navbar .container .nav-item .BillFather .BillHover");

// bill?.addEventListener("click", () => {
//   notification.classList.toggle("notificationshow");
//   bgBill.forEach((element) => {
//     element.classList.toggle("BillColor");
//   });
// });

// Form Section
var answerQuestionOneElements = document.querySelectorAll('.formBody .form form .question1 .answers .answer');
console.log(answerQuestionOneElements)

answerQuestionOneElements.forEach(function(answerElement) {
    answerElement.addEventListener('click', function() {
        answerQuestionOneElements.forEach(function(element) {
            element.querySelector('.formBody .form form .question1 .answers .answer .circle').classList.remove('choose');
          });
        answerElement.querySelector('.formBody .form form .question1 .answers .answer .circle').classList.toggle('choose');
        
      });
});

var answerQuestionTwoElements = document.querySelectorAll('.formBody .form form .question2 .answers .answer');

answerQuestionTwoElements.forEach(function(answerElement) {
    answerElement.addEventListener('click', function() {
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

