import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GradeCardComponent } from './grade-card.component';

describe('GradeCardComponent', () => {
  let component: GradeCardComponent;
  let fixture: ComponentFixture<GradeCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GradeCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GradeCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
