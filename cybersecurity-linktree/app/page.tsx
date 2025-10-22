import { Shield, Github, Linkedin, FileText, Award } from "lucide-react"

export default function Page() {
  const links = [
    {
      title: "ROOT ME",
      description: "Profil & Challenges",
      href: "https://www.root-me.org/ygp4ph?inc=statistiques&lang=fr",
      icon: Award,
    },
    {
      title: "GITHUB",
      description: "Projets & Code",
      href: "https://github.com/ygp4ph",
      icon: Github,
    },
    {
      title: "LINKEDIN",
      description: "Profil Professionnel",
      href: "https://www.linkedin.com/in/rapha%C3%ABl-couvert-267706338/",
      icon: Linkedin,
    },
    {
      title: "WRITE-UPS",
      description: "Challenges & Solutions",
      href: "https://ember-scilla-836.notion.site/Chals-284aa764c45c8036a986d25f1eeb3880",
      icon: FileText,
    },
  ]

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border">
        <div className="container mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-serif text-2xl tracking-[0.2em] text-foreground">RAPHAËL COUVERT</h1>
              <p className="mt-1 font-mono text-xs tracking-[0.15em] text-muted-foreground">CYBERSÉCURITÉ</p>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="border-b border-border">
        <div className="container mx-auto px-6 py-16">
          <div className="mx-auto max-w-2xl text-center">
            <div className="mb-8 flex justify-center">
              <div className="flex h-32 w-32 items-center justify-center border-2 border-border bg-background">
                <Shield className="h-16 w-16 text-foreground" strokeWidth={1.5} />
              </div>
            </div>

            <h2 className="font-serif text-4xl tracking-[0.15em] text-foreground">RAPHAËL COUVERT</h2>

            <p className="mt-6 font-mono text-sm tracking-[0.1em] text-foreground">ÉTUDIANT B2 CYBERSÉCURITÉ</p>

            <p className="mt-2 font-mono text-xs tracking-[0.1em] text-muted-foreground">BORDEAUX YNOV CAMPUS</p>

            <div className="mx-auto mt-8 max-w-xl border-t border-border pt-8">
              <p className="font-mono text-xs leading-relaxed tracking-[0.05em] text-muted-foreground">
                À LA RECHERCHE D'UN STAGE ET ALTERNANCE DÈS JUIN 2026
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Links Section */}
      <section className="py-16">
        <div className="container mx-auto px-6">
          <h3 className="mb-12 text-center font-serif text-2xl tracking-[0.2em] text-foreground">LIENS</h3>

          <div className="mx-auto grid max-w-3xl grid-cols-1 border border-border md:grid-cols-2">
            {links.map((link, index) => {
              const Icon = link.icon
              const isLastOdd = links.length % 2 !== 0 && index === links.length - 1

              return (
                <a
                  key={link.href}
                  href={link.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`group relative flex items-center justify-between border-border bg-background p-8 transition-colors hover:bg-muted ${
                    index % 2 === 0 ? "md:border-r" : ""
                  } ${
                    index < links.length - 2 || (index === links.length - 2 && !isLastOdd) ? "border-b" : ""
                  } ${isLastOdd ? "md:col-span-2" : ""}`}
                >
                  <div className="flex items-center gap-6">
                    <div className="flex h-12 w-12 items-center justify-center border border-border bg-background transition-colors group-hover:border-foreground">
                      <Icon className="h-5 w-5 text-foreground" strokeWidth={1.5} />
                    </div>

                    <div>
                      <h4 className="font-mono text-sm tracking-[0.15em] text-foreground">{link.title}</h4>
                      <p className="mt-1 font-mono text-xs tracking-[0.05em] text-muted-foreground">
                        {link.description}
                      </p>
                    </div>
                  </div>

                  <div className="transition-transform group-hover:translate-x-1">
                    <svg
                      className="h-5 w-5 text-muted-foreground"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={1.5}
                    >
                      <path strokeLinecap="square" strokeLinejoin="miter" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </div>
                </a>
              )
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border">
        <div className="container mx-auto px-6 py-8">
          <p className="text-center font-mono text-xs tracking-[0.1em] text-muted-foreground">© 2025 RAPHAËL COUVERT</p>
        </div>
      </footer>
    </main>
  )
}
