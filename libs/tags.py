#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# arxiv - arxiv plugin for calibre
# Copyright 2012 Abdó Roig-Maranges <abdo.roig@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re



_arxiv_tags ={
  'astro-ph.CO':          ['physics', 'cosmology'],
  'astro-ph.EP':          ['physics', 'astrophysics'],
  'astro-ph.GA':          ['physics', 'astrophysics'],
  'astro-ph.HE':          ['physics', 'astrophysics'],
  'astro-ph.IM':          ['physics', 'astrophysics', 'experimental'],
  'astro-ph.SR':          ['physics', 'astrophysics'],

  'cond-mat.dis-nn':      ['physics', 'condensed matter'],
  'cond-mat.mtrl-sci':    ['physics', 'condensed matter'],
  'cond-mat.mes-hall':    ['physics', 'condensed matter'],
  'cond-mat.other':       ['physics', 'condensed matter'],
  'cond-mat.quant-gas':   ['physics', 'condensed matter'],
  'cond-mat.soft':        ['physics', 'condensed matter'],
  'cond-mat.stat-mech':   ['physics', 'statistical mechanics'],
  'cond-mat.str-el':      ['physics', 'condensed matter'],
  'cond-mat.supr-con':    ['physics', 'condensed matter', 'superconductors'],

  'gr-qc':                ['physics', 'general relativity'],
  'hep-ex':               ['physics', 'experimental', 'particle physics'],
  'hep-lat':              ['physics', 'experimental', 'particle physics', 'lattice'],
  'hep-ph':               ['physics', 'phenomenology', 'particle physics'],
  'hep-th':               ['physics', 'qft', 'particle physics'],
  'math-ph':              ['physics'],
  'nucl-ex':              ['physics', 'experimental', 'nuclear physics'],
  'nucl-th':              ['physics', 'nuclear physics'],

  'physics.acc-ph':       ['physics', 'experimental', 'particle physics', 'particle accelerators'],
  'physics.ao-ph':        ['physics', 'atmospheric physics'],
  'physics.atom-ph':      ['physics', 'atomic physics'],
  'physics.atm-clus':     ['physics', 'atomic physics'],
  'physics.bio-ph':       ['physics', 'biological physics'],
  'physics.chem-ph':      ['physics', 'chemical physics'],
  'physics.class-ph':     ['physics', 'classical mechanics'],
  'physics.comp-ph':      ['physics', 'computational physics'],
  'physics.data-an':      ['physics', 'statistics'],
  'physics.flu-dyn':      ['physics', 'fluid dynamics'],
  'physics.gen-ph':       ['physics'],
  'physics.geo-ph':       ['physics', 'geophysics'],
  'physics.hist-ph':      ['physics', 'history'],
  'physics.ins-det':      ['physics', 'instrumentation', 'experimental'],
  'physics.med-ph':       ['physics', 'medical physics'],
  'physics.optics':       ['physics', 'optics'],
  'physics.ed-ph':        ['physics', 'education'],
  'physics.soc-ph':       ['physics', 'sociology'],
  'physics.plasm-ph':     ['physics', 'plasma'],
  'physics.pop-ph':       ['physics', 'divulgation'],
  'physics.space-ph':     ['physics'],

  'quant-ph':             ['physics', 'quantum mechanics'],

  'math.AG':              ['maths', 'algebraic geometry'],
  'math.AT':              ['maths', 'algebraic topology'],
  'math.AP':              ['maths', 'analysis', 'pde'],
  'math.CT':              ['maths', 'category theory'],
  'math.CA':              ['maths', 'analysis'],
  'math.CO':              ['maths', 'combinatorics'],
  'math.AC':              ['maths', 'algebra', 'commutative algebra'],
  'math.CV':              ['maths', 'analysis', 'complex analysis'],
  'math.DG':              ['maths', 'differential geometry'],
  'math.DS':              ['maths', 'analysis', 'dynamical systems'],
  'math.FA':              ['maths', 'functional analysis'],
  'math.GM':              ['maths'],
  'math.GN':              ['maths', 'topology'],
  'math.GT':              ['maths', 'geometric topology'],
  'math.GR':              ['maths', 'group theory'],
  'math.HO':              ['maths', 'history'],
  'math.IT':              ['maths', 'information theory'],
  'math.KT':              ['maths', 'K-theory'],
  'math.LO':              ['maths', 'logic'],
  'math.MP':              ['maths', 'physics'],
  'math.MG':              ['maths', 'metric geometry'],
  'math.NT':              ['maths', 'number theory'],
  'math.NA':              ['maths', 'numerical methods'],
  'math.OA':              ['maths', 'operator algebras', 'functional analysis'],
  'math.OC':              ['maths', 'optimization'],
  'math.PR':              ['maths', 'probability'],
  'math.QA':              ['maths', 'algebra', 'quantum algebra'],
  'math.RT':              ['maths', 'algebra', 'representation theory'],
  'math.RA':              ['maths', 'algebra', 'associative algebra'],
  'math.SP':              ['maths', 'functional analysis'],
  'math.ST':              ['maths', 'statistics'],
  'math.SG':              ['maths', 'differential geometry', 'symplectic geometry']

  # TODO: Nonlinear Sciences
  # TODO: Computer Science
  # TODO: Quantitative Biology
  # TODO: Quantitative Finance
  # TODO: Statistics
}

def arxiv_tags(subj):
    return _arxiv_tags.get(subj, [])



_msc_tags = {
    '03':                  ['logic'],
    '05':                  ['combinatorics'],
    '06':                  ['algebra'],
    '08':                  ['algebra'],
    '11':                  ['number theory'],
    '13':                  ['commutative algebra'],
    '14':                  ['algebraic geometry'],
    '16':                  ['algebra'],
    '19':                  ['K-theory'],

    '53':                  ['differential geometry'],
    '54':                  ['topology'],
    '55':                  ['topology'],
    '57':                  ['topology'],
    '58':                  ['geometric analysis'],
    '60':                  ['probability']
}


def msc_tags(subj):

    tags = set()
    m = re.match('([0-9]+)([A-Z]+)([0-9]+)', subj)

    if m:
        level1 = '%02d'   % int(m.group(1))
        level2 = '%s%s'   % (level1, m.group(2))
        level3 = '%s%02d' % (level2, int(m.group(3)))

        tags.update(_msc_tags.get(level1, []))
        tags.update(_msc_tags.get(level2, []))
        tags.update(_msc_tags.get(level3, []))

    return tags
