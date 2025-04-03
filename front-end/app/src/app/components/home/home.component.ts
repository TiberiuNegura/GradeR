import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-home',
  imports: [
    FormsModule,
    CommonModule
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  searchQuery: string = '';
  currentYear: number = new Date().getFullYear();
  isTeacher: boolean = true;
  
  categories = [
    {
      id: 1,
      name: 'Arts & Humanities',
      description: 'Literature, Philosophy, History, and more',
      icon: '🎭'
    },
    {
      id: 2,
      name: 'Science & Mathematics',
      description: 'Physics, Chemistry, Biology, Mathematics',
      icon: '🔬'
    },
    {
      id: 3,
      name: 'Social Sciences',
      description: 'Psychology, Sociology, Economics, and more',
      icon: '🌐'
    },
    {
      id: 4,
      name: 'Engineering & Technology',
      description: 'Computer Science, Civil, Electrical Engineering',
      icon: '💻'
    },
    {
      id: 5,
      name: 'Business & Management',
      description: 'Finance, Marketing, Accounting, and more',
      icon: '📊'
    },
    {
      id: 6,
      name: 'Health & Medicine',
      description: 'Nursing, Public Health, Medicine',
      icon: '🏥'
    }
  ];
  
  featuredCourses = [
    {
      id: 101,
      title: 'Introduction to Computer Science',
      code: 'CS 101',
      credits: 4,
      description: 'An introductory course covering fundamentals of programming and computational thinking.',
      imageText: 'Computer Science'
    },
    {
      id: 102,
      title: 'Principles of Economics',
      code: 'ECON 201',
      credits: 3,
      description: 'Study of economic principles, theories, and methods used in modern economics.',
      imageText: 'Economics'
    },
    {
      id: 103,
      title: 'General Biology',
      code: 'BIO 110',
      credits: 4,
      description: 'Introduction to biological concepts including cellular structure, genetics, and evolution.',
      imageText: 'Biology'
    },
    {
      id: 104,
      title: 'Art History: Renaissance to Modern',
      code: 'ART 205',
      credits: 3,
      description: 'Survey of major artistic movements from the Renaissance period to the modern era.',
      imageText: 'Art History'
    },
    {
      id: 105,
      title: 'Calculus I',
      code: 'MATH 141',
      credits: 4,
      description: 'Study of functions, limits, derivatives, and integrals with applications.',
      imageText: 'Mathematics'
    }
  ];
  
  quickLinks = [
    {
      id: 1,
      title: 'Academic Calendar',
      description: 'Important dates and deadlines',
      icon: '📅',
      url: '/calendar'
    },
    {
      id: 2,
      title: 'Registration',
      description: 'Register for courses',
      icon: '📝',
      url: '/registration'
    },
    {
      id: 3,
      title: 'Student Resources',
      description: 'Tools for academic success',
      icon: '🧰',
      url: '/resources'
    },
    {
      id: 4,
      title: 'Financial Aid',
      description: 'Scholarships and aid information',
      icon: '💰',
      url: '/financial-aid'
    }
  ];
  
  constructor(
    private router: Router,
    private route: ActivatedRoute
  ) { }
  
  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const role = params['role'] === 'true';
      console.log('Role:', role);

      this.isTeacher = role;
    });
  }
  
  performSearch(): void {
    if (this.searchQuery.trim()) {
      console.log('Searching for:', this.searchQuery);
      // In a real application, navigate to search results
      // this.router.navigate(['/search'], { queryParams: { q: this.searchQuery } });
    }
  }
  
  navigateToCategory(category: any): void {
    console.log('Navigating to category:', category.name);
    // In a real application, navigate to category page
    // this.router.navigate(['/category', category.id]);
  }
  
  enrollCourse(course: any): void {
    console.log('Viewing course details:', course.title);
    // In a real application, navigate to course details page
    // this.router.navigate(['/course', course.id]);
  }
  
  navigateToLink(link: any): void {
    console.log('Navigating to link:', link.title);
    // In a real application, navigate to the page
    // this.router.navigate([link.url]);
  }
}
