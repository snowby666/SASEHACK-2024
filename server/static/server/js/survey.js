$(document).ready(function(){
	$("#footer1").hide();
	$("#footer2").hide();
});

$('#s1-next').click(function(){
	jQuery('#sform1').addClass('d-none');
	jQuery('#sform2').removeClass('d-none');
  });

$('#s2-prev').click(function(){
jQuery('#sform2').addClass('d-none');
jQuery('#sform1').removeClass('d-none');
	});

$('#s2-next').click(function(){
	jQuery('#sform2').addClass('d-none');
	jQuery('#sform3').removeClass('d-none');
	});

$('#s3-prev').click(function(){
	jQuery('#sform3').addClass('d-none');
	jQuery('#sform2').removeClass('d-none');
	});
	
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" dotactive", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " dotactive";
}
class CustomSelect {
	constructor(originalSelect) {
	  this.originalSelect = originalSelect;
	  this.customSelect = document.createElement("div");
	  this.customSelect.classList.add("select");
  
	  this.originalSelect.querySelectorAll("option").forEach((optionElement) => {
		const itemElement = document.createElement("div");
  
		itemElement.classList.add("select__item");
		itemElement.textContent = optionElement.textContent;
		this.customSelect.appendChild(itemElement);
  
		if (optionElement.selected) {
		  this._select(itemElement);
		}
  
		itemElement.addEventListener("click", () => {
		  if (
			this.originalSelect.multiple &&
			itemElement.classList.contains("select__item--selected")
		  ) {
			this._deselect(itemElement);
		  } else {
			this._select(itemElement);
		  }
		});
	  });
  
	  this.originalSelect.insertAdjacentElement("afterend", this.customSelect);
	  this.originalSelect.style.display = "none";
	}
  
	_select(itemElement) {
	  const index = Array.from(this.customSelect.children).indexOf(itemElement);
  
	  if (!this.originalSelect.multiple) {
		this.customSelect.querySelectorAll(".select__item").forEach((el) => {
		  el.classList.remove("select__item--selected");
		  $("#footer1").hide();
		  $("#footer2").hide();
		});
	  }
  
	  this.originalSelect.querySelectorAll("option")[index].selected = true;
	  itemElement.classList.add("select__item--selected");
	  $("#footer1").show();
	  $("#footer2").show();
	}
  
	_deselect(itemElement) {
	  const index = Array.from(this.customSelect.children).indexOf(itemElement);
  
	  this.originalSelect.querySelectorAll("option")[index].selected = false;
	  itemElement.classList.remove("select__item--selected");
	  $("#footer1").hide();
	  $("#footer2").hide();
	}
  }
  
  document.querySelectorAll(".custom-select").forEach((selectElement) => {
	new CustomSelect(selectElement);
  });
