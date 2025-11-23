// ==========================================
// FLEXWORK AGENCY - MAIN JAVASCRIPT
// Modern, Interactive, Animated
// ==========================================

// ========== NAVIGATION ========== //
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Add shadow when scrolled
    if (scrollTop > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScrollTop = scrollTop;
});

// Mobile Menu Toggle
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Smooth Scroll to Section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Active Nav Link on Scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// ========== PORTFOLIO ========== //
const portfolioData = [
    {
        id: 1,
        title: 'E-Commerce Platform',
        category: 'web',
        icon: '🛒',
        description: 'Modern online shopping experience'
    },
    {
        id: 2,
        title: 'Mobile Banking App',
        category: 'app',
        icon: '📱',
        description: 'Secure financial management'
    },
    {
        id: 3,
        title: 'Brand Identity Design',
        category: 'branding',
        icon: '🎨',
        description: 'Complete brand overhaul'
    },
    {
        id: 4,
        title: 'Corporate Video',
        category: 'video',
        icon: '🎬',
        description: 'Engaging company presentation'
    },
    {
        id: 5,
        title: 'Restaurant Website',
        category: 'web',
        icon: '🍽️',
        description: 'Appetizing digital presence'
    },
    {
        id: 6,
        title: 'Fitness Tracker App',
        category: 'app',
        icon: '💪',
        description: 'Health & wellness companion'
    },
    {
        id: 7,
        title: 'Product Packaging',
        category: 'branding',
        icon: '📦',
        description: 'Eye-catching package design'
    },
    {
        id: 8,
        title: 'YouTube Channel',
        category: 'video',
        icon: '📺',
        description: 'Complete video editing service'
    },
    {
        id: 9,
        title: 'SaaS Dashboard',
        category: 'web',
        icon: '📊',
        description: 'Data visualization platform'
    }
];

// Render Portfolio Items
function renderPortfolio(filter = 'all') {
    const portfolioGrid = document.getElementById('portfolioGrid');
    portfolioGrid.innerHTML = '';
    
    const filteredItems = filter === 'all' 
        ? portfolioData 
        : portfolioData.filter(item => item.category === filter);
    
    filteredItems.forEach((item, index) => {
        const portfolioItem = document.createElement('div');
        portfolioItem.className = 'portfolio-item';
        portfolioItem.style.animation = `fadeIn 0.5s ease-out ${index * 0.1}s both`;
        
        portfolioItem.innerHTML = `
            <div class="portfolio-image">${item.icon}</div>
            <div class="portfolio-content">
                <h3 class="portfolio-title">${item.title}</h3>
                <p class="portfolio-category">${item.description}</p>
            </div>
        `;
        
        portfolioGrid.appendChild(portfolioItem);
    });
}

// Portfolio Filter Buttons
const filterButtons = document.querySelectorAll('.filter-btn');
filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        filterButtons.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        // Get filter value
        const filter = btn.getAttribute('data-filter');
        // Render filtered portfolio
        renderPortfolio(filter);
    });
});

// Initial portfolio render
document.addEventListener('DOMContentLoaded', () => {
    renderPortfolio();
});

// ========== MODALS ========== //
function showContactModal() {
    const modal = document.getElementById('contactModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function showLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function showSignupModal() {
    closeModal('loginModal');
    // You can create a signup modal similar to login
    alert('Signup functionality coming soon!');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
});

// ========== SERVICE MODAL ========== //
function openServiceModal(serviceType) {
    const serviceInfo = {
        'web-development': {
            title: 'Web Development Services',
            description: 'Build modern, responsive, and high-performing websites and web applications.',
            features: [
                'Custom website development',
                'E-commerce solutions',
                'Content Management Systems',
                'Web application development',
                'API integration',
                'SEO optimization'
            ],
            pricing: 'Starting from ₹15,000'
        },
        'graphic-design': {
            title: 'Graphic Design Services',
            description: 'Create stunning visual identities that capture your brand essence.',
            features: [
                'Logo & brand identity',
                'UI/UX design',
                'Marketing materials',
                'Social media graphics',
                'Print design',
                'Illustrations'
            ],
            pricing: 'Starting from ₹5,000'
        },
        'app-development': {
            title: 'Mobile App Development',
            description: 'Develop native and cross-platform mobile applications.',
            features: [
                'iOS app development',
                'Android app development',
                'Cross-platform apps (React Native, Flutter)',
                'App UI/UX design',
                'App Store optimization',
                'Backend development'
            ],
            pricing: 'Starting from ₹50,000'
        },
        'video-editing': {
            title: 'Video Editing Services',
            description: 'Professional video editing for all your content needs.',
            features: [
                'YouTube video editing',
                'Promotional videos',
                'Corporate videos',
                'Motion graphics',
                'Color grading',
                'VFX and animations'
            ],
            pricing: 'Starting from ₹3,000/video'
        },
        'content-writing': {
            title: 'Content Writing Services',
            description: 'Engaging, SEO-optimized content that converts.',
            features: [
                'Blog posts & articles',
                'Website copywriting',
                'SEO content',
                'Technical writing',
                'Product descriptions',
                'Email newsletters'
            ],
            pricing: 'Starting from ₹500/article'
        },
        'digital-marketing': {
            title: 'Digital Marketing Services',
            description: 'Grow your online presence with data-driven strategies.',
            features: [
                'Search Engine Optimization (SEO)',
                'Social media marketing',
                'Google Ads campaigns',
                'Email marketing',
                'Analytics & reporting',
                'Content strategy'
            ],
            pricing: 'Starting from ₹20,000/month'
        }
    };
    
    const service = serviceInfo[serviceType];
    
    if (service) {
        const featuresHTML = service.features.map(f => `<li>✓ ${f}</li>`).join('');
        
        alert(`${service.title}\n\n${service.description}\n\nKey Features:\n${service.features.join('\n')}\n\n${service.pricing}\n\nContact us to get started!`);
        
        // In a production app, you'd show a proper modal instead of alert
        showContactModal();
    }
}

// ========== PRICING ========== //
function selectPlan(planType) {
    const plans = {
        'starter': 'Starter Plan - ₹10,000',
        'professional': 'Professional Plan - ₹25,000',
        'enterprise': 'Enterprise Plan - Custom Pricing'
    };
    
    if (planType === 'enterprise') {
        alert(`You've selected the ${plans[planType]}. Let's discuss your requirements!`);
    } else {
        alert(`You've selected the ${plans[planType]}. Let's get started!`);
    }
    
    showContactModal();
}

// ========== FORM SUBMISSIONS ========== //
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        
        // Show success message
        alert('Thank you for your project submission! We will get back to you within 24 hours.');
        
        // Close modal
        closeModal('contactModal');
        
        // Reset form
        contactForm.reset();
        
        // In production, you would send this data to your backend
        console.log('Form submitted:', Object.fromEntries(formData));
    });
}

// ========== ANIMATIONS ON SCROLL ========== //
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and sections
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.service-card, .process-step, .pricing-card');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// ========== STATS COUNTER ANIMATION ========== //
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start) + '+';
        }
    }, 16);
}

// Animate stats when in viewport
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const target = parseInt(stat.textContent);
                animateCounter(stat, target);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
    statsObserver.observe(heroStats);
}

// ========== PARTICLE BACKGROUND (OPTIONAL) ========== //
// You can add this for extra wow factor
function createParticles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 2px;
            background: rgba(99, 102, 241, 0.5);
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float ${3 + Math.random() * 4}s ease-in-out infinite;
            animation-delay: ${Math.random() * 2}s;
        `;
        hero.appendChild(particle);
    }
}

// Uncomment to enable particles
// createParticles();

// ========== UTILITY FUNCTIONS ========== //
// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ========== KEYBOARD SHORTCUTS ========== //
document.addEventListener('keydown', (e) => {
    // ESC to close modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        });
    }
});

// ========== LOADING ANIMATION ========== //
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

console.log('🚀 FlexWork Agency - Website Loaded Successfully!');
