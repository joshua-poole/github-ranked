import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from '@/components/ui/navigation-menu'
import { Link } from '@tanstack/react-router'
import ThemeToggle from './ThemeToggle'

const navItems = [
  { label: 'Home', path: '/' },
  { label: 'Leaderboard', path: '/' },
  { label: 'About', path: '/' },
]

export default function Header() {
  return (
    <header className="w-full flex flex-row bg-secondary items-center justify-between p-5">
      <NavigationMenu className="gap-5">
        <h1 className="font-bold">GITRANK.GG</h1>
        <NavigationMenuList>
          {navItems.map((el) => (
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Link to={el.path}>{el.label}</Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
          ))}
        </NavigationMenuList>
      </NavigationMenu>
      <ThemeToggle />
    </header>
  )
}
