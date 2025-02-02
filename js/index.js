const heightChangeSpeed = 0.3;

//COURSE DIS

const lineClamp = 3;

var coursedisStartHeight = 0;
const coursedis = Array.from(document.getElementsByClassName("coursedis"));
const coursedisdictionary = coursedis.reduce((acc, key) => {
    acc.set(key, false);
    return acc;
}, new Map());

for(const _coursedis of coursedis){
    _coursedis.style.transition = `height ${heightChangeSpeed}s ease`;
    _coursedis.style.webkitLineClamp = `${lineClamp}`;
    _coursedis.style.lineClamp = `${lineClamp}`;

    _coursedis.addEventListener('mouseenter', OnDisHover);
    _coursedis.addEventListener('mouseleave', OnDisHoverLeave);
}

function OnDisHover(event) {
    const targetElement = event.currentTarget;
    coursedisStartHeight = targetElement.offsetHeight;

    targetElement.style.webkitLineClamp = `none`;
    targetElement.style.lineClamp = `none`;

    targetElement.style.height = `${coursedisStartHeight}px`;
    var endHeight = targetElement.scrollHeight;
    targetElement.style.height = `${endHeight}px`;

    coursedisdictionary.set(targetElement, true);
}

function OnDisHoverLeave(event) {
    const targetElement = event.currentTarget;
    targetElement.style.height = `${coursedisStartHeight}px`;

    coursedisdictionary.set(targetElement, false);
    setTimeout(() => { OnDisHoverLeave2(targetElement); }, heightChangeSpeed * 1000);
}

function OnDisHoverLeave2(targetElement) {
    if(coursedisdictionary.get(targetElement) == false){
        targetElement.style.webkitLineClamp = `${lineClamp}`;
        targetElement.style.lineClamp = `${lineClamp}`;
        targetElement.style.height = '';
    }
}

//COURSE FOR

var courseforStartHeight = 0;
const coursefor = Array.from(document.getElementsByClassName("courseinfoflexelementfor"));
const coursefordictionary = coursefor.reduce((acc, key) => {
    acc.set(key, false);
    return acc;
}, new Map());

window.addEventListener('resize', OnPreResizeFor);

for (const _coursefor of coursefor) {
    _coursefor.style.transition = `height ${heightChangeSpeed}s ease`;
    _coursefor.querySelector('.courseinfofor').style.display = 'none';
    courseforStartHeight =  _coursefor.querySelector('.courseinfofor0').offsetHeight;
    _coursefor.addEventListener('mouseenter', OnForHover);
    _coursefor.addEventListener('mouseleave', OnForHoverLeave);
}

function OnPreResizeFor()
{
    setTimeout(OnResizeFor, 10);
}

function OnResizeFor()
{
    Array.from(document.getElementsByClassName("courseinfoflexelementfor"))[0].style.height = '';
    courseforStartHeight = Array.from(document.getElementsByClassName("courseinfoflexelementfor"))[0].querySelector('.courseinfofor0').offsetHeight;
}

function OnForHover(event) {
    const targetElement = event.currentTarget;
    const coursethreepoints = targetElement.querySelector('.courseinfoflexelementforpoints');
    coursethreepoints.style.display = 'none';

    const courseforlist = targetElement.querySelector('.courseinfofor');
    courseforlist.style.display = '';

    targetElement.style.height = `${courseforStartHeight}px`;
    var endHeight = targetElement.scrollHeight;
    targetElement.style.height = `${endHeight}px`;

    courseauthorsdictionary.set(targetElement, true);
}

function OnForHoverLeave(event) {
    const targetElement = event.currentTarget;
    targetElement.style.height = `${courseforStartHeight}px`;
    courseauthorsdictionary.set(targetElement, false);
    setTimeout(() => { OnForHoverLeave2(targetElement); }, heightChangeSpeed * 1000);
}

function OnForHoverLeave2(targetElement) {
    if(courseauthorsdictionary.get(targetElement) == false){
        const coursethreepoints = targetElement.querySelector('.courseinfoflexelementforpoints');
        const courseforlist = targetElement.querySelector('.courseinfofor');

        coursethreepoints.style.display = '';
        courseforlist.style.display = 'none';
        targetElement.style.height = '';
    }
}

//COURSE AUTHORS

var courseauthorsStartHeight = 0;
const courseauthors = Array.from(document.getElementsByClassName("courseauthorsnames"));
const courseauthorsdictionary = courseauthors.reduce((acc, key) => {
    acc.set(key, false);
    return acc;
}, new Map());

for (const _courseauthors of courseauthors) {
    _courseauthors.style.transition = `height ${heightChangeSpeed}s ease`;
    _courseauthors.addEventListener('mouseenter', OnAuthorsHover);
    _courseauthors.addEventListener('mouseleave', OnAuthorsHoverLeave);
}

function OnAuthorsHover(event) {
    const targetElement = event.currentTarget;
    courseauthorsStartHeight = targetElement.querySelector('p').offsetHeight;
    targetElement.classList.add("courseauthorsnameshover");
    targetElement.style.height = `${courseauthorsStartHeight}px`;
    var endHeight = targetElement.scrollHeight;
    targetElement.style.height = `${endHeight}px`;

    courseauthorsdictionary.set(targetElement, true);
}

function OnAuthorsHoverLeave(event) {
    event.currentTarget.style.height = `${courseauthorsStartHeight}px`;
    const targetElement = event.currentTarget;
    courseauthorsdictionary.set(targetElement, false);
    setTimeout(() => { OnAuthorsHoverLeave2(targetElement); }, heightChangeSpeed * 1000);
}

function OnAuthorsHoverLeave2(targetElement) {
    if(courseauthorsdictionary.get(targetElement) == false){
        targetElement.classList.remove("courseauthorsnameshover");
        targetElement.style.height = '';
    }
}

//FILTER

var filterIsOpen = false;
const searchfieldtafilterbutton = document.getElementById('searchfieldtafilterbutton');
const searchfilterfield = document.getElementById('searchfiltersfield');
var currentopenfilter = 'none';

function setFilter(aElement) {
    if (aElement.classList.contains('setfilter')) {
        aElement.classList.remove('setfilter');
    }
    else {
        aElement.classList.add('setfilter');
    }
}

function openFilter() {
    filterIsOpen = !filterIsOpen;

    if (filterIsOpen) {
        searchfieldtafilterbutton.style.backgroundImage = 'url(../images/filterop.png)';
        searchfilterfield.classList.remove('searchfieldhidden');
        searchfilterfield.classList.add('searchfield');
    }
    else {
        searchfieldtafilterbutton.style.backgroundImage = 'url(../images/filter.png)';
        searchfilterfield.classList.remove('searchfield');
        searchfilterfield.classList.add('searchfieldhidden');

        var scrollDiv = searchfilterfield.querySelector('.searchfilterfieldscroll');
        if (hasHorizontalScrollbar(scrollDiv)) {
            scrollDiv.style.position = 'relative';
            scrollDiv.style.top = '0.2vw';
        }

        if (currentopenfilter != 'none') {
            openFilter2(currentopenfilter.id);
        }
    }
}

function openFilter2(id) {
    var newCurrentopenfilter = document.getElementById(id);

    if (currentopenfilter != 'none') {
        currentopenfilter.classList.remove('searchfield');
        currentopenfilter.classList.add('searchfieldhidden');
    }

    if (currentopenfilter != newCurrentopenfilter) {
        currentopenfilter = newCurrentopenfilter;
        currentopenfilter.classList.remove('searchfieldhidden');
        currentopenfilter.classList.add('searchfield');

        var scrollDiv = currentopenfilter.querySelector('.searchfilterfieldscroll');
        if (hasHorizontalScrollbar(scrollDiv)) {
            scrollDiv.style.position = 'relative';
            scrollDiv.style.top = '0.2vw';
        }
    }
    else {
        currentopenfilter = 'none';
    }
}

//MENU

function scrollToId(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}

let lastScrollTop = 0;
const myElement = document.getElementById('menu');

function hasHorizontalScrollbar(element) {
    return element.scrollWidth > element.clientWidth;
}

window.addEventListener('scroll', function () {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
        myElement.classList.add('hidden');
    } else {
        myElement.classList.remove('hidden');
    }
    lastScrollTop = scrollTop;
});