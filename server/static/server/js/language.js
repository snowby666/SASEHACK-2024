let el = $('.switch');
let cur = el.find('.current');
let options = el.find('.options li');
let content = $('#content');
let content2 = $('#content2');
let s1 = $('#s1');
let s2 = $('#s2');
let s3 = $('#s3');
let s4 = $('#s4');

// Open language dropdown panel

el.on('click', function(e) {
  el.addClass('show-options');
  
  setTimeout(function() {
    el.addClass('anim-options');
  }, 50);
  
  setTimeout(function() {
    el.addClass('show-shadow');
  }, 200);
});


// Close language dropdown panel

options.on('click', function(e) {
  e.stopPropagation();
  el.removeClass('anim-options');
  el.removeClass('show-shadow');
  
  let newLang = $(this).data('lang');
  
  cur.find('span').text(newLang);
  content.attr('class', newLang);
  content2.attr('class', newLang);
  s1.attr('class', newLang);
  s2.attr('class', newLang);
  s3.attr('class', newLang);
  s4.attr('class', newLang);
  
  setLang(newLang);
  
  options.removeClass('selected');
  $(this).addClass('selected');
  
  setTimeout(function() {
    el.removeClass('show-options');
  }, 600);

  if (newLang == 'vi'){
    $('#message').attr("placeholder", "Nhập tin nhắn ...")
  } else {
    $('#message').attr("placeholder", "Type your message ...")
  }
});


// Save selected options into Local Storage

function getLang() {
  let lang;
  if (localStorage.getItem('currentLang') === null) {
    lang = cur.find('span').text();
  } else {
    lang = JSON.parse(localStorage.getItem('currentLang')).toLowerCase();
  }
  
  // console.log(lang);

  cur.find('span').text(lang);
  options.parent().find(`li[data-lang="${lang}"]`).addClass('selected');
  
  content.attr('class', lang);
  content2.attr('class', lang);
  s1.attr('class', lang);
  s2.attr('class', lang);
  s3.attr('class', lang);
  s4.attr('class', lang);
}

getLang();

function setLang(newLang) {
    localStorage.setItem('currentLang', JSON.stringify(newLang).toLowerCase());
  
  content.attr('class', newLang);
  content2.attr('class', newLang);
  s1.attr('class', newLang);
  s2.attr('class', newLang);
  s3.attr('class', newLang);
  s4.attr('class', newLang);
  // console.log('New language is: ' + newLang);
}