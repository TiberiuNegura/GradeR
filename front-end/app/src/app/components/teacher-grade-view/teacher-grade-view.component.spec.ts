import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherGradeViewComponent } from './teacher-grade-view.component';

describe('TeacherGradeViewComponent', () => {
  let component: TeacherGradeViewComponent;
  let fixture: ComponentFixture<TeacherGradeViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeacherGradeViewComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TeacherGradeViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
