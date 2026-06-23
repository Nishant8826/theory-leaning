# Angular Material

## What is it?
Angular Material ek official UI component library hai jise Angular core team develop aur maintain karti hai. Yeh Google ke **Material Design** specifications guidelines ko implement karti hai aur developer ko pre-built, fully accessible aur customizable UI components (jaise tables, sliders, dialog boxes, aur menus) ka collection provide karti hai.

## Why do we need it?
Complex components (jaise access-friendly dialogs, sliding menus, ya paginated tables) ko scratch se HTML/CSS se banana behad time-consuming aur tedious task hai. Isme manually ARIA labels (accessibility), keyboard navigation rules, aur response styles handle karne padte hain. Angular Material in pre-tested components ko out of the box deta hai, jisse developers direct main app logic par focus kar saken.

```
Development from scratch:
Write custom layout ──> Write accessible HTML/ARIA ──> Implement keyboard controls ──> Add styling (months of effort)

With Angular Material:
Import MatTableModule ──> Bind data source ──> Access, responsiveness, and styles handled automatically
```

## How does it work?
1. **Component Imports**: Standalone components direct dynamic modules (jaise `MatButtonModule` ya `MatTableModule`) import karte hain.
2. **Theming (SASS)**: Built-in SASS dynamic mixins ke through components ke themes, colors, aur typography ko centralize aur customize kiya ja sakta hai.
3. **Accessibility (A11y)**: Angular CDK (Component Dev Kit) accessibility APIs follow karti hai jisse screen readers aur keyboard controls custom widgets par automatically map ho jate hain.

## Impact
* **Application Architecture**: Pre-built standardized widgets ke chalte development speed boost hoti hai aur custom configurations minimal ho jati hain.
* **Performance**: Modular structure (module-per-component) ke chalte sirf wahi components import hote hain jo application me use kiye gaye hain, jisse final bundle size small rehta hai.
* **Maintainability**: Centralized theming colors aur layouts standard dynamic SCSS variable maps ke through pure application me easily maintain ho jate hain.

## Real World Example
Jaise client dashboard page me data display karne ke liye hum `MatTable` aur `MatPaginator` use karte hain. Isse column sorting aur dynamic pagination responsive behavior ke sath instantly configure ho jate hain.

## Syntax
* **Adding Angular Material**: `ng add @angular/material`
* **Importing Material Component**:
```typescript
import { MatButtonModule } from '@angular/material/button';
```
* **Declaring Button**: `<button mat-raised-button color="primary">Click Me</button>`

## Code Examples
Neeche Angular Material Dialog popup aur Table component use karne ka complete example code structure diya gaya hai:

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
1. **Avoid Storing Dialog States Globally**: Dialog/Modal ke reference state ko hamesha local component controls me hi manage karein. `MatDialogRef` ko global state stores me inject karna avoid karein.
2. **Leverage the Angular CDK**: Custom UI elements (jaise overlays ya drag-drop list layouts) likhte waqt Angular CDK use karein, jisse behavior handling automatic ho jaye aur extra custom markup likhne ki zaroorat na ho.
3. **Use SCSS Mixins for Theming**: Component colors aur customization change karne ke liye Angular Material SCSS mixins configure karein. Direct class overwrites aur `!important` tags ka use control karein.

## Common Mistakes
* **Writing Custom CSS Overrides**: Component default visual properties ko brute-force styling class se override karna, jisse future version upgrades ke dauran UI compatibility breaks ho sakte hain.
* **Importing Unused Modules**: Pure Material library components (jaise `MatAutocompleteModule`) ko bina utilization ke templates imports me configure karna, jisse page startup bundle increase ho jaye.

## Interview Questions & Answers
### Q: What is the Angular CDK and how does it relate to Angular Material?
**A**: Angular CDK (Component Dev Kit) behaviors aur interactions manage karne ka framework utility library hai. Yeh core styles aur design constraints se free hai, jisse developers access controls, overlay systems, aur tables layouts ko bina material defaults visual patterns force kiye dynamic customize kar sakein.

### Q: How do you pass data into an Angular Material Dialog?
**A**: Dialog open karte waqt config object parameters me `data` property assign karke, aur dialog component constructor me `MAT_DIALOG_DATA` injection token ke zariye data inject kar liya jata hai.

## Summary
Angular Material Google material standard applications design ke tools customize karta hai. CDK utilities aur modular elements bundle optimizations visual components designs ko dynamic control settings apply aur manage karne ke options provide karte hain.

---

Previous : [Authentication and Authorization](./19_Authentication_and_Authorization.md) | Index : [Home](./00_index.md) | Next : [Performance Optimization](./21_Performance_Optimization.md)
