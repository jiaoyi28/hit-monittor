type NavItem = {
  href: string;
  label: string;
};

const navItems: NavItem[] = [
  { href: "#/", label: "总览" },
  { href: "#/repositories", label: "仓库" },
  { href: "#/settings", label: "配置" },
];

export function AppShell() {
  return (
    <div>
      <header>
        <h1>hit-monittor</h1>
        <nav aria-label="主导航">
          <ul>
            {navItems.map((item) => (
              <li key={item.href}>
                <a href={item.href}>{item.label}</a>
              </li>
            ))}
          </ul>
        </nav>
      </header>
    </div>
  );
}
