# Angular Material

## What is it?
Angular Material ek official UI component library hai jise Angular core team develop aur maintain karti hai. Yeh Google ke **Material Design** specifications guidelines ko implement karti hai aur developer ko pre-built, fully accessible aur customizable UI components (jaise tables, sliders, dialog boxes, aur menus) ka collection provide karti hai.

## Why do we need it?
Complex components (jaise access-friendly dialogs, sliding menus, ya dynamic paginated tables) ko HTML/CSS scratch se banana time-consuming aur tedious task hai. Aapko manually ARIA labels accessibility, keyboard navigation shortcuts, aur screen layouts handle karne padte hain. Angular Material in pre-tested components ko out of the box deta hai, jisse developers framework design coordinates badle bina main application rules and coding par focus kar sakte hain.

```
Development from scratch:
Write custom layout ──> Write accessible HTML/ARIA ──> Implement keyboard controls ──> Add styling (months of effort)

With Angular Material:
Import MatTableModule ──> Bind data source ──> Access, responsiveness, and styles handled automatically
```

## How does it work?
1. **Component Imports**: Standalone components direct dynamic modules (jaise `MatButtonModule` ya `MatTableModule`) import karte hain.
2. **Theming (SASS)**: Components layout styles parameters colors, fonts, margins controls configure karne ke liye built-in SASS dynamic mixins setup compile options use karti hai.
3. **Accessibility (A11y)**: Angular CDK (Component Dev Kit) utility systems follow karti hai jo elements transitions keyboard controls aur screen reader dynamic instructions pre-handle rakhte hain.

## Impact
* **Application Architecture**: Pre-built standardized widgets templates standard layout setups build karne me speed boost deta hai.
* **Performance**: Modular structure follow karta hai. Iska matlab hai ki aapko complete package compile karne ki zaroorat nahi hai, jo files compile components dynamic chunks package size thin rakhte hain.
* **Maintainability**: Centralized designs coordinates colors codes locations handle ho jati hain dynamic SCSS maps options ke zariye.

## Real World Example
Enterprise application client dashboard data reports display karne ke liye Angular Material `MatTable` aur `MatPaginator` use karta hai. Column sorting aur mobile pages layout transitions background systems self-optimize kar page rendering complete kar dete hain.

## Syntax
* **Adding Angular Material**: `ng add @angular/material`
* **Importing Material Component**:
```typescript
import { MatButtonModule } from '@angular/material/button';
```
* **Declaring Button**: `<button mat-raised-button color="primary">Click Me</button>`

## Code Examples
Neeche Angular Material Dialog popup aur dynamic Table integrate karne ka complete implementation details example code coordinate setup diya gaya hai:

```typescript
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatDialogModule, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

export interface UserElement {
  id: number;
  name: string;
  role: string;
}

const USER_DATA: UserElement[] = [
  { id: 1, name: 'Nishant', role: 'Architect' },
  { id: 2, name: 'Alice', role: 'Developer' },
  { id: 3, name: 'Bob', role: 'Designer' }
];

@Component({
  selector: 'app-user-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>Confirm Action</h2>
    <mat-dialog-content>Are you sure you want to modify this user?</mat-dialog-content>
    <mat-dialog-actions>
      <button mat-button (click)="close(false)">Cancel</button>
      <button mat-button color="warn" (click)="close(true)">Confirm</button>
    </mat-dialog-actions>
  `
})
export class UserDialogComponent {
  private dialogRef = inject(MatDialogRef<UserDialogComponent>);

  close(confirm: boolean) {
    this.dialogRef.close(confirm);
  }
}

@Component({
  selector: 'app-material-demo',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatButtonModule, MatDialogModule],
  template: `
    <div class="material-container">
      <h3>Active Team Directory</h3>
      
      <table mat-table [dataSource]="dataSource" class="mat-elevation-z2">
        <ng-container matColumnDef="id">
          <th mat-header-cell *header-cell-def> ID </th>
          <td mat-cell *mat-cell-def="let element"> {{element.id}} </td>
        </ng-container>

        <ng-container matColumnDef="name">
          <th mat-header-cell *header-cell-def> Name </th>
          <td mat-cell *mat-cell-def="let element"> {{element.name}} </td>
        </ng-container>

        <ng-container matColumnDef="role">
          <th mat-header-cell *header-cell-def> Role </th>
          <td mat-cell *mat-cell-def="let element"> {{element.role}} </td>
        </ng-container>

        <tr mat-header-row *mat-header-rowDef="displayedColumns"></tr>
        <tr mat-row *mat-rowDef="let row; columns: displayedColumns;" class="table-row"></tr>
      </table>

      <div class="actions">
        <button mat-raised-button color="primary" (click)="openDialog()">Modify Directory</button>
      </div>
    </div>
  `,
  styles: [`
    .material-container { padding: 20px; font-family: Roboto, sans-serif; }
    table { width: 100%; max-width: 500px; margin-bottom: 15px; }
    .table-row:hover { background: #f3f4f6; }
    .actions { margin-top: 15px; }
  `]
})
export class MaterialDemoComponent {
  private dialog = inject(MatDialog);

  displayedColumns: string[] = ['id', 'name', 'role'];
  dataSource = USER_DATA;

  openDialog() {
    const dialogRef = this.dialog.open(UserDialogComponent);

    dialogRef.afterClosed().subscribe(result => {
      console.log('Dialog choice result:', result);
    });
  }
}
```

## Best Practices
1. **Avoid Storing Dialog States Globally**: Modal states, dialog models pointers templates variables coordinates single components controllers me manage karein. `MatDialogRef` logic checks ko dynamic stores models variable setup me inject na karein.
2. **Leverage the Angular CDK**: Agar aap Material UI patterns custom layout styles implement karna chahte hain, toh direct Angular CDK options evaluate karein. Isse extra styles custom overriding overhead compile time warnings check prevent honge.
3. **Use SCSS Mixins for Theming**: Custom modifications parameters update themes styles setup ke liye SCSS mixins custom parameters files check use karein, direct CSS overwrite class blocks me `!important` markers avoid karein.

## Common Mistakes
* **Writing Custom CSS Overrides**: Component default styles override rules setup classes me force styles properties set karna. Yeh future versions coordinates upgrade compatibility warnings errors generate kar sakta hai.
* **Importing unnecessary modules**: Dynamic imports coordinate components declarations blocks me complete module elements classes library direct drag variables configurations configure karna.

## Interview Questions & Answers
### Q: What is the Angular CDK and how does it relate to Angular Material?
**A**: CDK behaviors mechanisms controls handles patterns framework utility pack hai jisme design styles colors specifications bounds override setups constraints parameters dependencies configuration models options target default templates styling setups pre-defined features checks define karte hain.

### Q: How do you pass data into an Angular Material Dialog?
**A**: Dialog constructor trigger coordinates configs properties checks setup me parameter option dynamic token input variables `MAT_DIALOG_DATA` token maps select logic properties define karke.

## Summary
Angular Material Angular applications Google design standards systems implementation tools provide karta hai. Modular directives files references inject configurations UI structure clean aur clean coordinate setups check build parameters dynamic parameters manage karte hain.

---

Previous : [Authentication and Authorization](./19_Authentication_and_Authorization.md) | Index : [Home](./00_index.md) | Next : [Performance Optimization](./21_Performance_Optimization.md)
