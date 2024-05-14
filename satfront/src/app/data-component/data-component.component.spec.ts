import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataComponentComponent } from './data-component.component';

describe('DataComponentComponent', () => {
  let component: DataComponentComponent;
  let fixture: ComponentFixture<DataComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DataComponentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DataComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
