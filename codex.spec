%bcond_without check
%bcond_without bootstrap
%global cargo_install_lib 0
%global crate_dir codex-rs/cli

Name:           codex
Version:        0.98.0
Release:        3
Summary:        OpenAI Codex command-line interface

License:        Apache-2.0
URL:            https://github.com/openai/codex
Source0:        %{url}/archive/refs/tags/rust-v%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  rust-packaging
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig(openssl)
BuildRequires:  git-core

%description
OpenAI Codex is a coding assistant that runs in your terminal.

%if %{without bootstrap}
%generate_buildrequires
cd %{crate_dir}
%cargo_generate_buildrequires
%endif

%prep
%autosetup -n codex-rust-v%{version}
cd %{crate_dir}

%if %{with bootstrap}
# Bootstrap pulls crates from the network with mock --enable-network
# because not all dependencies exist as Fedora crate RPMs yet
%cargo_prep -N
sed -i 's/offline = true/offline = false/' .cargo/config.toml
%else
%cargo_prep
%endif

%build
cd %{crate_dir}
%cargo_build

%install
cd %{crate_dir}
%cargo_install

# Shell completion files are generated from the built binary.
%{buildroot}%{_bindir}/codex completion bash > codex.bash
%{buildroot}%{_bindir}/codex completion fish > codex.fish
%{buildroot}%{_bindir}/codex completion zsh > _codex

install -Dpm 0644 codex.bash %{buildroot}%{bash_completions_dir}/codex
install -Dpm 0644 codex.fish %{buildroot}%{fish_completions_dir}/codex.fish
install -Dpm 0644 _codex %{buildroot}%{zsh_completions_dir}/_codex

%check
%if %{with check}
cd %{crate_dir}
%cargo_test
%{buildroot}%{_bindir}/codex --help >/dev/null
%endif

%files
%license LICENSE
%doc README.md
%doc codex-rs/README.md
%{_bindir}/codex
%{bash_completions_dir}/codex
%{fish_completions_dir}/codex.fish
%{zsh_completions_dir}/_codex

%changelog
* Wed Feb 11 2026 Ernesto Martinez <me@ecomaikgolf.com> - 0.98.0-1
- Maintain explicit changelog entry for wider chroot compatibility.
